import dash

app = dash.Dash(serve_locally=False)
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True