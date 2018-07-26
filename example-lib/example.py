from time import sleep
from classifier import SimpleClassifier

if __name__ == "__main__":
    s = SimpleClassifier(host='localhost', port=8080, proto="http")
    print("Classifier URI: ", s.uri)
    
    print("Get all available datasets: ", s.datasets.get())
    
    print("Get one  datasets: ", s.datasets.get(dataset='animals'))
    
    print("Create one dataset: ", s.datasets.create('animals'))
    # Add pictures
    print("Get one dataset: ", s.datasets.get('animals'))

    dogs_urls = [
        "https://farm4.staticflickr.com/3373/3600836516_ab924c6729_q_d.jpg",
        "https://farm4.staticflickr.com/3940/15473596487_5ed985dd35_q_d.jpg",
        "https://farm3.staticflickr.com/2905/32672915111_8e55c72707_q_d.jpg",
        "https://farm6.staticflickr.com/5259/5514206982_c8acb517ee_q_d.jpg",
        "https://farm9.staticflickr.com/8104/8631368705_907915f30e_q_d.jpg"
    ]
    cats_urls = [
        "https://farm8.staticflickr.com/7342/10373218496_4fc37d8e69_q_d.jpg",
        "https://farm4.staticflickr.com/3445/5695891871_a390aaa97b_q_d.jpg",
        "https://farm5.staticflickr.com/4373/36215281321_f7fc5b3632_q_d.jpg",
        "https://farm7.staticflickr.com/6082/6117272430_5b539f14fc_q_d.jpg",
        "https://farm1.staticflickr.com/471/18464362609_2b30e928a6_q_d.jpg"
    ]

    # print("Add pictures to one dataset with the dogs label:")
    
    # print(s.datasets.addPicture(dataset='animals', label='dogs', urls=dogs_urls))
    
    # print(s.datasets.addPicture(dataset='animals', label='cats', urls=cats_urls))
    
    # print("Launching dataset training: ",
    #       s.datasets.train('animals', training_steps=50))

    # print(s.datasets.get('animals'))

    # while s.datasets.get('animals')['trained'] == False:
    #     print('Waiting for dataset to be trained...')
    #     sleep(2)

    print('Dataset is trained.')

    print("Testing classifier with one picture: ")
    print(s.datasets.classify('animals', url="https://farm4.staticflickr.com/3380/3533802505_02f938ebd1_q_d.jpg"))
