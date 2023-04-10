from classes.Vehicles import GetVehicleBrand, GetVehicleModel, GetVehicleModelYear, GetVehicleDetails
from classes.Google import GCSUploader

vehicle_type = ["carros","caminhoes","motos"]
limit_executor = 3

for vtype in vehicle_type:
    vehicles = GetVehicleBrand(vtype)
    vehicles.get_vehicle_list()
    vehicles.save_to_file()

    for brand in vehicles.brands:
        vehicle_model = GetVehicleModel(vtype,brand["codigo"])
        vehicle_model.get_model_detail()
        vehicle_model.save_to_file()

        size_list = len(vehicle_model.models)
        limit_list = limit_executor if size_list > limit_executor else size_list

        for model in vehicle_model.models[0:limit_list]:
            vehicle_model_year = GetVehicleModelYear(vtype,brand["codigo"],model["codigo"])
            vehicle_model_year.get_year_detail()
            vehicle_model_year.save_to_file()

            for vehicle_detail in vehicle_model_year.years:
                vehicle_value = GetVehicleDetails(vtype,brand["codigo"],model["codigo"], vehicle_detail["codigo"])
                vehicle_value.get_detail()
                vehicle_value.save_to_file()
                print(vehicle_value.details)



