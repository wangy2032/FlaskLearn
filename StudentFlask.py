# -*- coding: utf-8 -*-

from StudentSystem import create_app

app = create_app('DevelopmentConfig')

if __name__=='__main__':
    app.run(debug=True)