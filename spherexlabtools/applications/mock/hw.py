sr830 = {
    "instance_name": "sr830",
    "manufacturer": "fakes",
    "instrument": "SwissArmyFake",
    "resource_name": 0.1
}

sr510 = {
    "instance_name": "sr510",
    "manufacturer": "fakes",
    "instrument": "SwissArmyFake",
    "resource_name": 0.1
}

Lockin = {
    "instance_name": "LockinAmp",
    "subinstruments": [
        sr510, sr830
    ]
}

Heater = {
    "instance_name": "Heater",
    "manufacturer": "fakes",
    "instrument": "SwissArmyFake",
    "resource_name": 0.1
}

Camera = {
    "instance_name": "Camera",
    "manufacturer": "fakes",
    "instrument": "SwissArmyFake",
    "resource_name": 0.1,
    "params": {
        "frame_format": "mono_16"
    }
}

SubclassInst = {
    "instance_name": "SubTest",
    "manufacturer": "submock",
    "instrument": "SwissArmyTripleSub",
    "resource_name": 0.1,
}

CompoundTesting = {
    "instance_name": "CompoundTest",
    "subinstruments": [
        SubclassInst, Camera, Heater
    ]
}

INSTRUMENT_SUITE = [Lockin, Heater, Camera, CompoundTesting]
