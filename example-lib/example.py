from time import sleep
from classifier import SimpleClassifier

if __name__ == "__main__":
    s = SimpleClassifier(host='localhost', port=8080, proto="http")
    print("Classifier URI: \n", s.uri)
    
    print("Get all available datasets: \n", s.datasets.get())
    
    print("Get one  datasets: \n", s.datasets.get(dataset='animals'))
    
    print("Create one dataset: \n", s.datasets.create('animals'))
    # Add pictures
    print("Get one dataset: \n", s.datasets.get('animals'))

    dogs_urls = [
        "https://farm4.staticflickr.com/3373/3600836516_ab924c6729_q_d.jpg",
        "https://farm4.staticflickr.com/3940/15473596487_5ed985dd35_q_d.jpg",
        "https://farm3.staticflickr.com/2905/32672915111_8e55c72707_q_d.jpg",
        "https://farm6.staticflickr.com/5259/5514206982_c8acb517ee_q_d.jpg",
        "https://farm9.staticflickr.com/8104/8631368705_907915f30e_q_d.jpg",
        "https://farm8.staticflickr.com/7054/6903859309_c4cfb4c3d6_q_d.jpg",
        "https://farm4.staticflickr.com/3818/10193880154_3b955e5cf6_q_d.jpg",
        "https://farm8.staticflickr.com/7366/16357144647_a4d5f5fcd4_q_d.jpg",
        "https://farm5.staticflickr.com/4480/23880791608_44654c8757_q_d.jpg",
        "https://farm6.staticflickr.com/5338/8849012494_f4561f8a45_q_d.jpg"
    ]

    cats_urls = [
        "https://farm8.staticflickr.com/7342/10373218496_4fc37d8e69_q_d.jpg",
        "https://farm4.staticflickr.com/3445/5695891871_a390aaa97b_q_d.jpg",
        "https://farm5.staticflickr.com/4373/36215281321_f7fc5b3632_q_d.jpg",
        "https://farm7.staticflickr.com/6082/6117272430_5b539f14fc_q_d.jpg",
        "https://farm1.staticflickr.com/471/18464362609_2b30e928a6_q_d.jpg",
        "https://farm5.staticflickr.com/4130/5026705021_d81d6cb09c_q_d.jpg",
        "https://farm4.staticflickr.com/3033/2588311068_5ae957c4e8_q_d.jpg",
        "https://farm1.staticflickr.com/22/29022259_c7807ce1e8_q_d.jpg",
        "https://farm7.staticflickr.com/6069/6116740631_b7c2424e0b_q_d.jpg",
        "https://farm5.staticflickr.com/4381/35543718933_23a68e2b6d_q_d.jpg"
    ]

    print("Add pictures to one dataset with the dogs label:\n")
    
    # Use of spaces for testing spaces in dataset names
    for i in range(2):
        print(s.datasets.addPicture(dataset='animals', label='beautiful dog', urls=dogs_urls))
    
        print(s.datasets.addPicture(dataset='animals',
                                    label='beautiful cat', urls=cats_urls))
    
    print("Launching dataset training: \n",
          s.datasets.train('animals', training_steps=50))

    print(s.datasets.get('animals'))

    while s.datasets.get('animals')['trained'] == False:
        print('Waiting for dataset to be trained...')
        sleep(2)

    print('Dataset is trained.\n')

    print("Testing classifier with one dog picture: \n")
    print(s.datasets.classify('animals', url="https://farm4.staticflickr.com/3380/3533802505_02f938ebd1_q_d.jpg"))

    print("Testing classifier with one cat picture: \n")
    print(s.datasets.classify('animals', url="https://farm1.staticflickr.com/51/169329862_b3b297c7a9_q_d.jpg"))

    print('Deleting the created dataset: \n')
    print(s.datasets.delete('animals'))
