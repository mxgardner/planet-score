from org.openlca.core.model import Process, ProductSystem
from org.openlca.app.result import CalculationResult
from org.openlca.app import LcaCalculation
from org.openlca.core.model import Category
from org.openlca.core.model import ImpactCategory

print("Retrieving process for Sugar - US...")
sugar_process = None
all_processes = db.getAll(Process)

for process in all_processes:
    if "Sugar" in process.name and "US" in process.name:
        sugar_process = process
        break

if not sugar_process:
    print("Sugar - US process not found in the database.")
    exit()

print(f"Found process: {sugar_process.name}")

product_system = ProductSystem()
product_system.name = sugar_process.name + " System"
product_system.referenceProcess = sugar_process

print("Setting up the LCA calculation with the CML 2001 method...")
lca_calculation = LcaCalculation(product_system)
lca_calculation.setImpactMethod("CML 2001") 

print("Running the LCA calculation...")
lca_result = lca_calculation.run()

gwp_result = None
for result in lca_result.getImpactResults():
    if isinstance(result, ImpactCategory) and "GWP" in result.name:
        gwp_result = result
        break

if gwp_result:
    print(f"GWP Result (kg CO2 eq): {gwp_result.value}")
else:
    print("GWP (Global Warming Potential) not found in the calculation result.")

total_gwp = gwp_result.value if gwp_result else None
print(f"Total GWP: {total_gwp} kg CO2 eq.")
