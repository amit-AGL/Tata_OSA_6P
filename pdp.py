# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go
from data_fetch import static_values, data_fetch

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data and a Graph'),
    # Button to trigger data refresh
    html.Button("Refresh Data", id="refresh-button", n_clicks=0),
    # DataTable to display the merged data
    dash_table.DataTable(id='data-table', page_size=5),
    # Graph to display the bar plot
    dcc.Graph(id='bar-plot')
])

# Callback to update data and components on button click
@app.callback(
    [Output('data-table', 'data'),
     Output('bar-plot', 'figure')],
    [Input('refresh-button', 'n_clicks')]
)
def update_data(n_clicks):
    # Fetch new data from the database when the button is clicked
    if n_clicks > 0:
        data = data_fetch()

        # Get static values
        static_df = static_values()

        # Merge data from database query with static values using a left join
        merged_data = pd.merge(static_df, data, on='pf_id', how='left').fillna(0)

        # Fill NaN values in 'count' column with corresponding 'static_count' values
        merged_data.loc[merged_data['count'].isna(), 'count'] = merged_data['static_count']

        # Calculate the difference between static and dynamic values
        merged_data['remaining'] = merged_data['static_count'] - merged_data['count']

        # Create bar plot
        fig = go.Figure()
        # Add bar for completed part (dynamic data)
        fig.add_trace(go.Bar(x=merged_data['pf_id'], y=merged_data['count'], name='Completed', marker_color='blue'))
        # Add bar for remaining part (difference between static and dynamic data)
        fig.add_trace(
            go.Bar(x=merged_data['pf_id'], y=merged_data['remaining'], name='Remaining', marker_color='orange'))
        # Update layout
        fig.update_layout(barmode='stack', title='Completed vs Remaining',
                          xaxis_title='pf_id', yaxis_title='Count')

        # Convert merged data to dict for DataTable
        data_table_data = merged_data.to_dict('records')

        # Return updated data and figure
        return data_table_data, fig

    # If refresh button is not clicked, return initial data and empty figure
    return static_values().to_dict('records'), go.Figure()


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
