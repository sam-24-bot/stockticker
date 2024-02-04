from flask import Flask, render_template_string, render_template, request
import requests

application = Flask(__name__,  template_folder = 'templates')

@application.route("/", methods=["GET"])
def index():
     if 'URL' not in request.args:
          value = request.form.get("myform")
          return render_template("index.html", value=value)
     else:
          ticker = request.args.get('URL', 'default_value')
          req = requests.get(f"https://api.tiingo.com/tiingo/daily/{ticker}?token=23532c1817f7f20ad49457837e0a4c681fad7fe2")
          summary = requests.get(f"https://api.tiingo.com/iex/{ticker}?token=23532c1817f7f20ad49457837e0a4c681fad7fe2")
          if req.status_code != 200 or summary.status_code != 200:
               return "Error: No record has been found, please enter a valid symbol."
          jsonfile = req.json()

          #company outlook tab json keys
          company_name = jsonfile.get("name", " ")
          stock_ticker = jsonfile.get("ticker", " ")
          stock_exchange_code = jsonfile.get("exchangeCode", " ")
          company_start_date = jsonfile.get("startDate", " ")
          #description needs to be truncated to only span the first 5 lines
          description = jsonfile.get("description", " ")

          summaryjson = summary.json()

          #stock summary tab json keys
          stock_ticker_symbol = summaryjson[0]["ticker"]
          trading_day = summaryjson[0]["timestamp"]
          trading_day = trading_day[:10]
          previous_closing_price = summaryjson[0]["prevClose"]
          opening_price = summaryjson[0]["open"]
          high_price = summaryjson[0]["high"]
          low_price = summaryjson[0]["low"]
          last_price = summaryjson[0]["last"]
          num_shares_traded = summaryjson[0]["volume"]

          change = last_price - previous_closing_price
          if previous_closing_price != 0:
               change_percent = (change/previous_closing_price) * 100
          else:
               change_percent = 0
          
          if(change < 0):
               change_arrow = """<img id="downarrow" alt="downarrow" src="./RedArrowDown.png" width="10%" height="10%">"""
          else:
               change_arrow = """<img id="uparrow" alt="uparrow" src="./GreenArrowUP.png" width="10%" height="10%">"""
        
          if(change_percent < 0):
               changepercent_arrow = """<img id="downarrow" alt="downarrow" src="./RedArrowDown.png" width="10%" height="10%">"""
          else:
               changepercent_arrow = """<img id="uparrow" alt="uparrow" src="./GreenArrowUP.png" width="10%" height="10%">"""
          
          change = "%.2f" % change
          change_percent = "%.2f" % change_percent

          js_code= """
          function openTable(tab) {
               var tab_selected = document.getElementsByClassName("tab_member");
               for (var i = 0; i < tab_selected.length; i++) {
                    tab_selected[i].style.display = "none";  
               }
               document.getElementById(tab).style.display = "block";  
          }
          """

          CSS_code="""
          table{
               border: 1px solid #999999;
               border-collapse: collapse;
               width:100%;
               height:80px;
          }

          td{
          border: 1px solid #999999;
          border-collapse: collapse;
          }
          
          th{
               background-color:#d8d8d8;
          }
          
          button{
               background-color:#d8d8d8;
          }
          
          #one{
          background-color:#d8d8d8;
          width: 40%;
          }
          #one_data{
          background-color:#ffffff;
          text-align: center;
          }
          
          #two{
          background-color:#d8d8d8;
          width: 40%;
          }
          #two_data{
          background-color:#ffffff;
          text-align: center;
          }
          
          #three{
          background-color:#d8d8d8;
          width: 40%;
          }
          #three_data{
          background-color:#ffffff;
          text-align: center;
          }
          
          #four{
          background-color:#d8d8d8;
          width: 40%;
          }
          #four_data{
          background-color:#ffffff;
          text-align: center;
          }
          
          #five{
          background-color:#d8d8d8;
          width: 40%;
          }
          #five_data{
          background-color:#ffffff;
          text-align: center;
          }
          
          #six{
          background-color:#d8d8d8;
          width: 40%;
          }
          #six_data{
          background-color:#ffffff;
          text-align: center;
          }
          
          #seven{
          background-color:#d8d8d8;
          width: 40%;
          }
          #seven_data{
          background-color:#ffffff;
          text-align: center;
          }
          
          #eight{
          background-color:#d8d8d8;
          width: 40%;
          }
          #eight_data{
          background-color:#ffffff;
          text-align: center;
          }
          
          #nine{
          background-color:#d8d8d8;
          width: 40%;
          }
          #nine_data{
          background-color:#ffffff;
          text-align: center;
          }
          
          #ten{
          background-color:#d8d8d8;
          width: 40%;
          }
          #ten_data{
          background-color:#ffffff;
          text-align: center;
          }
          
          #eleven{
          background-color:#d8d8d8;
          width: 40%;
          }
          #eleven_data{
          background-color:#ffffff;
          text-align: center;
          }
          
          #tweleve{
          background-color:#d8d8d8;
          width: 40%;
          }
          #tweleve_data{
          background-color:#ffffff;
          text-align: center;
          }

          #thirteen{
          background-color:#d8d8d8;
          width: 40%;
          }
          #thirteen_data{
          background-color:#ffffff;
          text-align: center;
          }
            
          #fourteen{
          background-color:#d8d8d8;
          width: 40%;
          }
          #fourteen_data{
          background-color:#ffffff;
          text-align: center;
          }

          #fifteen{
          background-color:#d8d8d8;
          width: 40%;
          }
          #fifteen_data{
          background-color:#ffffff;
          text-align: center;
          }
          """

          value = request.form.get("myform")
          rendered_template = render_template("index.html", value=value)

          html_code = f"""
          <!DOCTYPE html>
          <head>
          <style>{CSS_code}</style>
          </head>

          <body>
          <div class="tab">
          <button class="tab" onclick="openTable('Company Outlook')">Company Outlook</button>
          <button class="tab" onclick="openTable('Stock Summary')">Stock Summary</button>
          <button class="tab" onclick="openTable('Charts')">Charts</button>
          <button class="tab" onclick="openTable('Latest News')">Latest News</button>
          </div>
      
          <div id="Company Outlook" class="tab_member" style="display:none">
          <table id="table_one">
          <tr>
          <td id="one">Company Name</td>
          <td id="one_data" class="table_data">{company_name}</td>
          </tr>
    
          <tr>
          <td id="two">Stock Ticker Symbol</td>
          <td id="two_data" class="table_data">{stock_ticker}</td>
          </tr>
    
          <tr>
          <td id="three">Stock Exchange Code</td>
          <td id="three_data" class="table_data">{stock_exchange_code}</td></tr>
    
          <tr>
          <td id="four">Company Start Date</td>
          <td id="four_data" class="table_data">{company_start_date}</td></tr>
    
          <tr>
          <td id="five">Description</td>
          <td id="five_data" class="table_data">{description}</td></tr></table>
          </div>
          
          <div id="Stock Summary" class="tab_member" style="display:none">
          <table id="table_two">
          <tr>
          <td id="six">Stock Ticker Symbol</td>
          <td id="six_data" class="table_data">{stock_ticker_symbol}</td></tr>
          
          <tr>
          <td id="seven">Trading Day</td>
          <td id="seven_data" class="table_data">{trading_day}</td></tr>
    
          <tr>
          <td id="eight">Previous Closing Price</td>
          <td id="eight_data" class="table_data">{previous_closing_price}</td></tr>
     
          <tr>
          <td id="nine">Opening Price</td>
          <td id="nine_data" class="table_data">{opening_price}</td></tr>
    
          <tr>
          <td id="ten">High Price</td>
          <td id="ten_data" class="table_data">{high_price}</td></tr>
    
          <tr>
          <td id="eleven">Low Price</td>
          <td id="eleven_data" class="table_data">{low_price}</td></tr>
    
          <tr>
          <td id="tweleve">Last Price</td>
          <td id="tweleve_data" class="table_data">{last_price}</td></tr>

          <tr>
          <td id="thirteen">Change</td>
          <td id="thirteen_data" class="table_data">{change}{change_arrow}</td></tr>
    
          <tr>
          <td id="fourteen">Change Percent</td>
          <td id="fourteen_data" class="table_data">{change_percent}{changepercent_arrow}</td></tr>
    
          <tr>
          <td id="fifteen">Number of Shares Traded</td>
          <td id="fifteen_data" class="table_data">{num_shares_traded}</td></tr></table>
          </div>
          
          <div id="Charts" class="tab_member" style="display:none">
          </div>
          
          <div id="Latest News" class="tab_member" style="display:none">
          </div>

          <script>{js_code}</script>
          </body>
          </html>
          """
          html_string = rendered_template + html_code   
          return render_template_string(html_string)   
          
if __name__ == "__main__":
    #application.run(debug=True)
    application.run()


