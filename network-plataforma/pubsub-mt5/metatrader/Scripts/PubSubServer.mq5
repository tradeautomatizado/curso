//+------------------------------------------------------------------+
//|                                                 PubSubServer.mq5 |
//|                                                  Paulo Rodrigues |
//|                                     https://www.codekraft.com.br |
//+------------------------------------------------------------------+
#property copyright "Paulo Rodrigues"
#property link      "https://www.codekraft.com.br"
#property version   "1.00"

#include <Zmq/Zmq.mqh>
#include <Trade\SymbolInfo.mqh>

string PROJECT_NAME = "Python Stock Publisher";
string ZEROMQ_PROTOCOL = "tcp";
string HOSTNAME = "*";

int SUB_PORT;
int MILLISECOND_TIMER;
int MagicNumber = 12345678;

// CREATE ZeroMQ Context
Context context(PROJECT_NAME);


// CREATE ZMQ_SUB SOCKET
Socket server(context,ZMQ_PUB);

bool LoadSettings()
{
   MILLISECOND_TIMER = 1000;
   Print("Push Interval: " + IntegerToString(MILLISECOND_TIMER));   
   
   SUB_PORT = 5557;
   Print("Push Port: " + IntegerToString(SUB_PORT));     
   
   return(true);
}

//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
int OnInit(void)
  {
//---
   if (!LoadSettings()) return(INIT_FAILED);
   
   EventSetMillisecondTimer(MILLISECOND_TIMER);     // Set Millisecond Timer to get client socket input
   
   server.bind(StringFormat("%s://%s:%d", ZEROMQ_PROTOCOL, HOSTNAME, SUB_PORT));

   Print("[REP] Binding MT5 Server to Socket on Port " + IntegerToString(SUB_PORT) + "..");
      
    /*
        Maximum amount of time in milliseconds that the thread will try to send messages 
        after its socket has been closed (the default value of -1 means to linger forever):
    */
   
   server.setLinger(1000);  // 1000 milliseconds
   
   server.setSendHighWaterMark(5);     // 5 messages only.
   
   return(INIT_SUCCEEDED);
   
  }
//+------------------------------------------------------------------+

void OnCalculatePrice()
{

   Print("Getting rates...");
   
   MqlRates BarData[1]; 
   
   double value = 0;
      
   !SymbolInfoInteger(_Symbol,SYMBOL_SELECT);
   
   int copied = CopyRates(_Symbol, PERIOD_CURRENT, 0, 1, BarData); // Copy the data of last incomplete BAR  
     
   if (copied <= 0){
      CopyRates(_Symbol, PERIOD_D1, 0, 1, BarData); // Copy the data of last incomplete BAR      
   }   
   
   if (copied > 0)
   {
      value = BarData[0].close;
   }   
   
   server.send("%s %s");
   server.send(_Symbol+ " " + DoubleToString(value));   

   Print("[REP] Symbol sent.");   
       
}

//+------------------------------------------------------------------+
//| Expert timer function                                            |
//+------------------------------------------------------------------+
void OnTimer()
{   
   OnCalculatePrice();
}
//+------------------------------------------------------------------+
