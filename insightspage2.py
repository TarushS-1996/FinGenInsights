from model.finmodel import FinModel
import streamlit as st
import json
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

promptInsight = '''Generate a Python script that produces JSON data representing the financial information of a company and have the values be represented as integers. The JSON data should include the following key-value structure:

{
  "COMPANY_NAME": {
    "Total Net Revenue": {
      "3Q23": TOTAL_NET_REVENUE_3Q23,
      "2Q23": TOTAL_NET_REVENUE_2Q23,
      "1Q23": TOTAL_NET_REVENUE_1Q23,
      "4Q22": TOTAL_NET_REVENUE_4Q22,
      "3Q22": TOTAL_NET_REVENUE_3Q22
    },
    "Total Noninterest Expense": {
      "3Q23": TOTAL_NONINTEREST_EXPENSE_3Q23,
      "2Q23": TOTAL_NONINTEREST_EXPENSE_2Q23,
      "1Q23": TOTAL_NONINTEREST_EXPENSE_1Q23,
      "4Q22": TOTAL_NONINTEREST_EXPENSE_4Q22,
      "3Q22": TOTAL_NONINTEREST_EXPENSE_3Q22
    },
    "Pre-Provision Profit": {
      "3Q23": PRE_PROVISION_PROFIT_3Q23,
      "2Q23": PRE_PROVISION_PROFIT_2Q23,
      "1Q23": PRE_PROVISION_PROFIT_1Q23,
      "4Q22": PRE_PROVISION_PROFIT_4Q22,
      "3Q22": PRE_PROVISION_PROFIT_3Q22
    },
    "Provision for Credit Losses": {
      "3Q23": PROVISION_FOR_CREDIT_LOSSES_3Q23,
      "2Q23": PROVISION_FOR_CREDIT_LOSSES_2Q23,
      "1Q23": PROVISION_FOR_CREDIT_LOSSES_1Q23,
      "4Q22": PROVISION_FOR_CREDIT_LOSSES_4Q22,
      "3Q22": PROVISION_FOR_CREDIT_LOSSES_3Q22
    },
    "Net Income": {
      "3Q23": NET_INCOME_3Q23,
      "2Q23": NET_INCOME_2Q23,
      "1Q23": NET_INCOME_1Q23,
      "4Q22": NET_INCOME_4Q22,
      "3Q22": NET_INCOME_3Q22
    }
  }
}'''

# Remove commas from numbers in the JSON data
def remove_commas(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = remove_commas(value)
            elif isinstance(value, str):
                if ',' in value:
                    data[key] = int(value.replace(',', ''))
            elif isinstance(value, list):
                data[key] = [remove_commas(item) for item in value]
    return data

def insights_page2(model=None):
    if model is None:
        st.markdown('Please upload a PDF file to generate insights.')
        return
    
    # Add a button to navigate back to the chat page
    if st.button('Back to Chat'):
        st.session_state.selected = 'Chat'
        st.experimental_rerun()
    finModel = model
    insi = finModel.as_query_engine().query(promptInsight)
    
    json_data = json.dumps(insi.response, indent=2)
    json_data = insi.response.replace("'", '"')
    json_data = json.loads(json_data)
    data = json_data
    ### we get the name of the company and use that as title for the page
    company_name = list(data.keys())[0]
    st.title(f'Financial Insights for {company_name}')
    # Visualization code
    # Visualization 1: Line Chart for Total Net Revenue and Total Noninterest Expense Over Time
    quarters = list(data[company_name]['Total Net Revenue'].keys())
    total_net_revenue = list(data[company_name]['Total Net Revenue'].values())
    total_noninterest_expense = list(data[company_name]['Total Noninterest Expense'].values())
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=quarters, y=total_net_revenue, mode='lines+markers', name='Total Net Revenue'))
    fig1.add_trace(go.Scatter(x=quarters, y=total_noninterest_expense, mode='lines+markers', name='Total Noninterest Expense'))
    fig1.update_layout(title='Total Net Revenue and Total Noninterest Expense Over Time', xaxis_title='Quarter', yaxis_title='Amount')
    st.plotly_chart(fig1, use_container_width=True)
    
    # Visualization 2: Bar Chart for Pre-Provision Profit and Provision for Credit Losses
    pre_provision_profit = list(data[company_name]['Pre-Provision Profit'].values())
    provision_for_credit_losses = list(data[company_name]['Provision for Credit Losses'].values())
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=quarters, y=pre_provision_profit, name='Pre-Provision Profit'))
    fig2.add_trace(go.Bar(x=quarters, y=provision_for_credit_losses, name='Provision for Credit Losses', opacity=0.7))
    fig2.update_layout(title='Pre-Provision Profit vs. Provision for Credit Losses', xaxis_title='Quarter', yaxis_title='Amount', barmode='group')
    st.plotly_chart(fig2, use_container_width=True)
    
    # Visualization 3: Line Chart for Net Income Over Time
    net_income = list(data[company_name]['Net Income'].values())
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=quarters, y=net_income, mode='lines+markers', name='Net Income'))
    fig3.update_layout(title='Net Income Over Time', xaxis_title='Quarter', yaxis_title='Amount')
    st.plotly_chart(fig3, use_container_width=True)
    
    
    
    
if __name__ == '__main__':
    insights_page2(model=None)
    
