from abc import abstractmethod


class Machine:
    @abstractmethod
    def calc_mass(self):
        pass

    @abstractmethod
    def calc_front_axis_pressure(self):
        pass

    @abstractmethod
    def calc_back_axis_pressure(self):
        pass

    @abstractmethod
    def get_parameters(self, *args) -> dict:
        pass

    def __init__(self, name, number, calibration_data: dict):
        self.calibration_data = calibration_data
        self.name = name
        self.number = number


class Vehicle:
    def __init__(self):
        self.machines = []

    def add_machine(self, new_machine: Machine):
        self.machines.append(new_machine)

    def calculate_mass(self):
        return sum([machine.calc_mass() for machine in self.machines])

    def add_truck(self, truck_dict):
        """
        Function to add a truck to machine
        :param truck_dict: a dictionary contating fields:
        name: str
        number: str
        calibration: a dictionary, now should be just nothing in it
        info: just additional dictionaru for some fields, now can be nothing in it
        >>> Vehicle().add_truck({"name": "Ringo Star", "number": "(BG) AA2322XT", "calibration": dict(), "info": dict()})
        :return:
        """
        new_truck = Truck(truck_dict["name"], truck_dict["number"], truck_dict["calibration"], truck_dict["info"])
        self.add_machine(new_truck)


class Truck(Machine):
    def __init__(self, name, number, calibration_data: dict, truck_info: dict):
        super().__init__(name, number, calibration_data)
        self.info = truck_info


class Trailer(Machine):
    pass
