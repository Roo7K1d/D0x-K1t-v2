# Setup

The process of setting this webservice up is pretty straightforward and doesn't take a lot of time.

{% hint style="warning" %}
Make sure you have installed [Python 3](https://www.python.org/downloads/) or above on your operating system.
{% endhint %}

In order to download the tool this is what you will have to do:

```bash
# apt-get install git //if you haven't already installed git on your system.
git clone https://github.com/roo7k1d/D0x-K1t-v2 && cd D0x-K1t-v2
```

{% hint style="info" %}
This will download the latest version from GitHub and put it in the folder called "D0x-K1t-v2".
{% endhint %}

Now we just need to install all the requirements:

```bash
pip install -r requirements.txt
```

All you now only have left to do is to start your webserver:

```bash
python run.py
```

{% hint style="success" %}
Done! You're all set and can now access your freshly installed D0x-K1t-v2 via your browser by accessing `https://<your server ip>:5000`
{% endhint %}

