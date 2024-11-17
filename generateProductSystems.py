from olca_ipc import ipc

# Connect to the OpenLCA IPC server
PORT = 8080
print(f"Attempting to connect to OpenLCA IPC server on port {PORT}...")
client = ipc.Client(PORT)

# Verify the connection
try:
    client.call("ping")  # Simple ping to check if the connection is active
    print("Successfully connected to OpenLCA IPC server!")
except Exception as e:
    print("Failed to connect to OpenLCA IPC server. Please ensure it is running.")
    print(f"Error: {e}")
    exit()

# Retrieve all flows from the database
print("Retrieving all flows from the OpenLCA database...")
try:
    all_flows = client.get_all("Flow")  # Retrieve all flows
    print(f"Total flows retrieved: {len(all_flows)}")
except Exception as e:
    print("Error retrieving flows from the database.")
    print(f"Error: {e}")
    exit()

# Filter flows to include only those from EXIOBASE
exiobase_flows = [flow for flow in all_flows if flow.category and "EXIOBASE" in flow.category.name]
if not exiobase_flows:
    print("No EXIOBASE flows found in the database.")
    exit()

print(f"Found {len(exiobase_flows)} EXIOBASE flows. Generating processes and product systems...")

# Iterate through EXIOBASE flows and process each material-region pair
for flow in exiobase_flows:
    flow_name = flow.name  # Example: "Textiles (17) - AU"
    try:
        # Extract material and region from the flow name
        material, region = flow_name.split(" - ")
    except ValueError:
        print(f"Skipping flow '{flow_name}' due to unexpected name format.")
        continue

    # Define process and product system names
    process_name = f"{material} - {region}"
    product_system_name = f"{material} ({region}) System"

    # Check if the process already exists
    existing_process = client.find("Process", process_name)
    if not existing_process:
        try:
            # Create a new process
            process = ipc.Process()
            process.name = process_name
            process.category = flow.category  # Use the same category as the flow
            process.description = f"Process for {material} in {region}"

            # Add the input flow (monetary input)
            input_exchange = ipc.Exchange()
            input_exchange.flow = flow
            input_exchange.amount = 1.0  # 1 EUR
            input_exchange.input = True
            process.exchanges.append(input_exchange)

            # Create an output flow
            output_flow = ipc.Flow()
            output_flow.name = f"{material} ({region})"
            output_flow.flow_type = ipc.FlowType.PRODUCT_FLOW
            output_flow.unit = client.find("Unit", "kg")  # Use kilograms as the unit
            client.save(output_flow)

            # Add the output exchange
            output_exchange = ipc.Exchange()
            output_exchange.flow = output_flow
            output_exchange.amount = 1.0  # 1 kg
            output_exchange.input = False
            process.exchanges.append(output_exchange)

            # Save the process
            client.save(process)
            print(f"Process '{process_name}' created successfully.")
        except Exception as e:
            print(f"Failed to create process '{process_name}': {e}")
            continue
    else:
        print(f"Process '{process_name}' already exists. Skipping creation.")
        process = existing_process  # Reuse the existing process

    # Check if the product system already exists
    existing_system = client.find("ProductSystem", product_system_name)
    if not existing_system:
        try:
            # Create a product system
            product_system = ipc.ProductSystem()
            product_system.name = product_system_name
            product_system.process = process
            product_system.description = f"Product system for {material} in {region}"
            client.save(product_system)
            print(f"Product system '{product_system_name}' created successfully.")
        except Exception as e:
            print(f"Failed to create product system '{product_system_name}': {e}")
            continue
    else:
        print(f"Product system '{product_system_name}' already exists. Skipping.")

print("All processes and product systems have been created successfully.")
