from cognitive_cell.lego import CognitiveCellRequest, CognitiveCellV9

request = CognitiveCellRequest(
    statement="Blue colour is observed.",
    interaction_mode="workflow_component",
    autonomy_mode="log",
)

print("Import successful.")
print(request)
print(CognitiveCellV9)
