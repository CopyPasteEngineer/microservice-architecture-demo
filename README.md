# Microservice Architecture Demo
## โดย [Copy Paste Engineer](https://www.facebook.com/CopyPasteEng)

![](imgs/cover.png)

คลิปเนื้อหา: [ออกแบบ Microservices ด้วย Domain Driven Design #3 - Architecture Overview](https://youtu.be/EBjfiuJsYe4)

### Install
ติดตั้ง library สำหรับ `ordering service` และ `inventory service`

```bash
cd ordering/
pip install -r domain.requirements.txt
pip install -r infrastructure.requirements.txt
pip install -r rest.requirements.txt

cd ../inventory/
pip install -r domain.requirements.txt
pip install -r infrastructure.requirements.txt
pip install -r rest.requirements.txt
```

### วิธีรัน
ไปที่ folder นอกสุดของ project แล้วรันด้วย `docker-compose`

```bash
docker-compose up -d
```

### วิธีปิด

ไปที่ folder นอกสุดของ project แล้วปิดการทำงานด้วย `docker-compose`

```bash
docker-compose down
```
