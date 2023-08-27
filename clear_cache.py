from flask_caching import Cache

from api import app, config

cache = Cache()

def main():
    cache.init_app(app, config=your_cache_config)

    with app.app_context():
        cache.clear()

if __name__ == '__main__':
    main()