import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

external_stylesheets = [
    {
        "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384.MCw98/SF-nGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm82iuXoaPkFOJwJ8ERdknl.PMO",
        "crossorigin": "anonymous",
    }
]


patients= pd.read_csv('IndividualDetails.csv')
total = patients.shape[0]
active = patients[patients['current_status']=='Hospitalized'].shape[0]
recovered = patients[patients['current_status']=='Recovered'].shape[0]
deaths = patients[patients['current_status']=='Deceased'].shape[0]


options = [
	{'label' : 'All', 'value' : 'All'},
	{'label' : 'Hospitalized', 'value' : 'Hospitalized'},
	{'label' : 'Recovered', 'value' : 'Recovered'},
	{'label' : 'Deceased', 'value' : 'Deceased'}
]



c = pd.read_csv('covid_19_india.csv')
c['Date'] = pd.to_datetime(c['Date'], format="mixed")
c['month'] = c['Date'].dt.month

opts = [
	{'label' : 'All', 'value' : 'All'},
	{'label' : 'Cured', 'value' : 'cured'},
	{'label' : 'Confirmed', 'value' : 'confirmed'},
	{'label' : 'Deaths', 'value' : 'deaths'}
]



app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div([
	html.H1("Corona Virus Pandemic", style={'color' : '#fff', 'text-align' : 'center'}),
	
	html.Div([
	
		html.Div([
			html.Div([
				html.Div([
					html.H3("Total Cases", className="text-light"),
					html.H4(total, className="text-light")
				], className='card-body')
			], className='card bg-danger')
		], className='col-md-3'),
		
		html.Div([
			html.Div([
				html.Div([
					html.H3("Active Cases", className="text-light"),
					html.H4(active, className="text-light")
				], className='card-body')
			], className='card bg-info')
		], className='col-md-3'),
		
		html.Div([
			html.Div([
				html.Div([
					html.H3("Recovered", className="text-light"),
					html.H4(recovered, className="text-light")
				], className='card-body')
			], className='card bg-warning')
		], className='col-md-3'),
		
		html.Div([
			html.Div([
				html.Div([
					html.H3("Deaths", className="text-light"),
					html.H4(deaths, className="text-light")
				], className='card-body')
			], className='card bg-success')
		], className='col-md-3')
		
	], className='row'),
	
	html.Div([
		html.Div([
			html.Div([
				html.Div([
					dcc.Dropdown(id='picker1', options=opts, value='All'),
					dcc.Graph(id='bar1')
				], className='card-body')
			], className='card')
		], className='col-md-12')
	], className='row'),
	
	html.Div([
		html.Div([
			html.Div([
				html.Div([
					dcc.Dropdown(id='picker', options=options, value='All'),
					dcc.Graph(id='bar')
				], className='card-body')
			], className='card')
		], className='col-md-12')
	], className='row')
	
], className='container')


@app.callback(Output('bar', 'figure'), Input('picker', 'value'))
def update_graph(type):
	
	if type=='All':
		pbar = patients['detected_state'].value_counts().reset_index()
		x = pbar['detected_state']
		y = pbar['count']
		return {
			'data' : [go.Bar(x=x, y=y)],
			'layout' : go.Layout(title='State Total Count')
		}
	
	else:	
		npat = patients[patients['current_status']==type]
		pbar = npat['detected_state'].value_counts().reset_index()
		return {
			'data' : [go.Bar(x=pbar['detected_state'], y=pbar['count'])],
			'layout' : go.Layout(title='State Total Count')
		}

cured = c.groupby('month')['Cured'].sum().reset_index()
conf = c.groupby('month')['Confirmed'].sum().reset_index()
deaths = c.groupby('month')['Deaths'].sum().reset_index()

@app.callback(Output('bar1', 'figure'), Input('picker1', 'value'))
def update_graph1(type):
	
	if type=='All':
		data = [
		go.Bar(name='Cured', x=cured['month'], y=cured['Cured']),
		go.Bar(name='Deaths', x=deaths['month'], y=deaths['Deaths']),
		go.Bar(name='Confirmed', x=conf['month'], y=conf['Confirmed'])
]
		return {
			'data' : data,
			'layout' : go.Layout(title='Monthly Data')
		}
	
	elif type=="Cured":
		data = [go.Bar(x=cured['month'],y=cured['Cured'])]
		return {
			'data' : data,
			'layout' : go.Layout(title='Monthly Data')
		}
	
	elif type=='Confirmed':
		data = [go.Bar(x=conf['month'], y=conf['Confirmed'])]
		return {
			'data' : data,
			'layout' : go.Layout(title='Monthly Data')
		}
	
	else:
		data = [go.Bar(x=deaths['month'], y=deaths['Deaths'])]
		return {
			'data' : data,
			'layout' : go.Layout(title='Monthly Data')
		}

if __name__ == "__main__":
	app.run_server(debug=True)