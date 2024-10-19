from reload.service.ComponentManagementService import ComponentManagementService
from reload.service.TrayService import TrayService
from server_io.service.FileService import FileService


BIN_SIZE = 8


file_service = FileService()
tray_service = TrayService()
component_management_service = ComponentManagementService()

brasses = file_service.open_component_file("brasses_")
brass_bins = component_management_service.sort_into_competition_bins(brasses, 0.75, BIN_SIZE)

bullets = file_service.open_component_file("bullets_")
bullet_lengths = list(map(lambda x: x[1], bullets))
bullet_bins = component_management_service.sort_into_competition_bins(bullet_lengths, 0.01, BIN_SIZE)

powders = file_service.open_component_file("powders_")
powder_bins = component_management_service.sort_into_competition_bins(powders, 0.003, BIN_SIZE)

smallest_bin_size = min(len(brass_bins), len(bullet_bins), len(powder_bins))
print()

for i in range(smallest_bin_size):
  print(f"Bin #{i+1}")
  tray_service.print_bin("Brass", brass_bins[i])
  tray_service.print_bin("Bullet", bullet_bins[i])
  tray_service.print_bin("Powder", powder_bins[i])
  input()
