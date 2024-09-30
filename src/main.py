from projects.mvp.random_service import RandomService, generate_dataset

if __name__ == "__main__":
    for d in generate_dataset():
        print("result: ", RandomService.generate(d))
