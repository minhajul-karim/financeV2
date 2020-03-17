"""Compile static assets."""

from flask_assets import Bundle


def compile_assets(assets):
    """Configure and build asset bundles."""
    css_bundle = Bundle("src/css/*.css",
                        filters="cssmin",
                        output="build/css/all_styles.css")

    js_bundle = Bundle("src/js/jquery-3.3.1.min.js",
                       "src/js/bootstrap.min.js",
                       "src/js/popper.min.js",
                       "src/js/myscript.js",
                       filters="jsmin",
                       output="build/js/all_js.js")

    # Register and build assets
    assets.register("all_styles", css_bundle)
    assets.register("all_js", js_bundle)
    css_bundle.build()
    js_bundle.build()
