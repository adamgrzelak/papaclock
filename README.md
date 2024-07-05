# PapaClock

It's always <code>21:37</code> somewhere...

### Description

The application shows a list of places where the current local time
approaches 21:37 (9:37 p.m.).

### Deployment

#### Local

1. Install requirements.

```
pip install -r requirements.txt
```

2. Run the application.

```
gunicorn wsgi:app
```

© AG 2024
