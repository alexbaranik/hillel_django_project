from shop.celery import app


@app.task
def test_task():
    print('Test')
