# zenoh-as-a-service
This work intends to create some production-ready examples of [Zenoh](http://zenoh.io/). 


### Todo in this project
- [x] Create ABC class
- [x] Create base class for Zenoh Native
- [x] Create base class for Zenoh Network
- [x] Create base Zenoh Native and Net for Pub/Sub
- [x] Make some examples for Zenoh Pub/Sub
    - [x] Pub/Sub in a single PC
    - [x] Pub/Sub in a network via TCP connection with Zenoh-Net
- [ ] Performance measurements
    - [ ] Benchmark of sending image data in a single PC (image & Custom image)
        - [ ] Proc. Latency to send image (encode + sending)
        - [ ] Proc. Latency to retrieve image (retrieve + decode)
        - [ ] Communication Latency to send image data
    - [ ] Benchmark of sending image data in a network, between two hosts  (image & Custom image)
        - [ ] Proc. Latency to send image (encode + sending)
        - [ ] Proc. Latency to retrieve image (retrieve + decode)
        - [ ] Communication Latency to send image data
        - [ ] Bandwidth usage per second
    - [ ] Head-to-head comparison for streaming image-typed data:
        - [ ] ImageZMQ (ZeroMQ)
            - [ ] sending normal images 
            - [ ] sending images with a custom encoder
        - [ ] Redis Pub/Sub 
            - [ ] sending normal images 
            - [ ] sending images with a custom encoder 
        - [ ] Kafka
            - [ ] sending normal images 
            - [ ] sending images with a custom encoder 

### Environment reccomendation
- Linux (tested in Ubuntu 18.04 ++)

### Pre-requirements
1. Python version >=3.6 ([related issue](https://github.com/eclipse-zenoh/zenoh-python/commit/0e9b37780730b13b827e949e941922f53e5626b4))
2. Install python virtual environment: `$ python3 -m venv venv`
    - Please upgrade the version: `$ pip install --uppgrade pip`
3. Install [Rust toolchain](https://rustup.rs/)
    - Install rustop: `$ sudo snap install rustup --classic`
    - Instal toolchain: `$ rustup toolchain install nightly`
4. Install [maturin](https://github.com/PyO3/maturin): `$ pip install maturin`
5. Core Python library: `$ pip install -r requirements.txt`