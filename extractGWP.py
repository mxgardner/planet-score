from org.openlca.core.model import Process, ProductSystem
from org.openlca.app.result import CalculationResult
from org.openlca.app import LcaCalculation
from org.openlca.core.model import Category
from org.openlca.core.model import ImpactCategory

# Step 1: Retrieve the process for Sugar - US (adjust as necessary)
print("Retrieving process for Sugar - US...")
sugar_process = None
all_processes = db.getAll(Process)

# Searching for the 'Sugar - US' process (or any other process you need)
for process in all_processes:
    if "Sugar" in process.name and "US" in process.name:
        sugar_process = process
        break

if not sugar_process:
    print("Sugar - US process not found in the database.")
    exit()

print(f"Found process: {sugar_process.name}")

# Step 2: Set up the Product System for this process
product_system = ProductSystem()
product_system.name = sugar_process.name + " System"
product_system.referenceProcess = sugar_process

# Step 3: Set up the LCA calculation with the CML 2001 impact assessment method
print("Setting up the LCA calculation with the CML 2001 method...")
lca_calculation = LcaCalculation(product_system)
lca_calculation.setImpactMethod("CML 2001")  # Select the CML 2001 method for impact assessment

# Step 4: Run the LCA calculation
print("Running the LCA calculation...")
lca_result = lca_calculation.run()

# Step 5: Extract the GWP (Global Warming Potential) result from the LCA calculation
gwp_result = None
for result in lca_result.getImpactResults():
    if isinstance(result, ImpactCategory) and "GWP" in result.name:
        gwp_result = result
        break

if gwp_result:
    print(f"GWP Result (kg CO2 eq): {gwp_result.value}")
else:
    print("GWP (Global Warming Potential) not found in the calculation result.")

# Step 6: Return the GWP value for further use (e.g., in your Chrome extension)
total_gwp = gwp_result.value if gwp_result else None
print(f"Total GWP: {total_gwp} kg CO2 eq.")
