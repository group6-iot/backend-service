import pickle


def predict(humidity: float, light: float):
    model = pickle.load(open("ai/soil_moisture.sav", "rb"))
    print(humidity, light)
    return model.predict([[int(light), int(humidity)]])