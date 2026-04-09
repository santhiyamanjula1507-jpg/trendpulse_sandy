def predict(x):
    return x * 2

if __name__ == "__main__":
    value = int(input("Enter a number: "))
    result = predict(value)
    print("Prediction:", result)