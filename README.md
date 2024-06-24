# Dev Assessment - Webhook Receiver

Please use this repository for constructing the Flask webhook receiver.
x
*******************
x
## Setupx

* Create a new virtual environmentx

```bash
pip install virtualenv
```x

* Create the virtual env
x
```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

You need to use this as the base and setup the flask app. Integrate this with MongoDB (commented at `app/extensions.py`)

*******************
