<center> # Strategic Proposal # </center>

# Carbon Tax influence on Export Dynamics & Traffic Forecasting #
## I. Research Methodology ##

The objective is to establish a data-driven correlation between macroeconomic indicators, specific merchandise flow, and logistical traffic volumes.

1. Market Identification: Identify the top 10 export destinations to determine primary trade corridors.

2. Product Analysis: Catalog the top 10 export commodities (by HS Code) to understand weight-to-value ratios and shipping requirements.

3. Trend Mapping: Analyze the historical export performance of these commodities over a 5–10 year horizon to identify cyclicality.

3. Predictive Modeling: Utilize macroeconomic forecasting models (incorporating GDP growth, exchange rates, and PMI) to project future volumes.

### Key Premise ####
Cargo traffic volume is treated as a high-correlation proxy for export vitality; changes in trade orders are leading indicators for logistics demand.


## II. Integrated Database & Resources ##
1. Taiwan National Data (Primary)

  1.1 經濟部國際貿易署 > 海關進出口統計 > 貿易統計 > 資料庫查詢 > 綜合查詢 https://portal.sw.nat.gov.tw/APGA/GA30

  1.2 財政部貿易調查統計 https://web02.mof.gov.tw/njswww/WebMain.aspx?sys=100&funid=defjsptgl

  1.3 海關開放資料集(Open Data) (連結：關務資料開放平臺) https://data.gov.tw/datasets/search?p=1&size=10&s=_score_desc&rat=436,688,33987
 
2. Global Trade & Tariff Intelligence (WTO)

   2.1 Tariff & Import Notifications (IDB): Detailed data on applied tariffs and imports by country. https://ttd.wto.org/en/data/idb

   2.2 WTO Commitments (CTS): Information on bound tariffs and service commitments. https://ttd.wto.org/en/data/cts

   2.3 U.S. DataWeb U.S. Trade & Tariff Data https://dataweb.usitc.gov/
   The USITC DataWeb provides public access to the official U.S. import and export statistics of the U.S. Department of Commerce in a user-friendly web interface. Using the DataWeb querying tool, users can build custom queries and access these data in a spreadsheet or a web-based format.
      - Tariff Database https://dataweb.usitc.gov/tariff/database
      Search for individual tariff lines using HTS category numbers or product descriptions.
      - Tariff Annual Data https://dataweb.usitc.gov/tariff/annual
      Access annual tariff data from 1997 to present available in a downloadable zip file format.
      - Tariff Programs https://dataweb.usitc.gov/tariff/programs
      View listings of U.S. trade agreements and programs with reduced/no tariffs on eligible goods.
   
   2.4 Ranking of the top trading partners of the United States for trade goods in 2024, by import value  https://www.statista.com/statistics/186601/ranking-of-the-largest-trading-partners-for-us-imports/

3. IMF (International Monetary Fund): For World Economic Outlook (WEO) reports and global GDP projections.

4. OECD: For composite leading indicators (CLI) and structural economic analysis of developed markets.

5. Analysis of the Transmission of Carbon Tax using a Multi-Sector Dynamic Stochastic General Equilibrium Model
   Kohei Matsumura, et.al.
   https://www.boj.or.jp/en/research/wps_rev/wps_2023/data/wp23e02.pdf

6. Prophet: This is a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. It works best with time series that have strong seasonal effects and several seasons of historical data. Prophet is robust to missing data and shifts in the trend, and typically handles outliers well.

    Prophet is open source software released by Facebook's Core Data Science team. It is available for download on CRAN and PyPI. https://github.com/facebook/prophet

8. DIY Macroeconomic Model Simulation: This website provides free pedagogical resources and source codes for macroeconomic model simulation. It follows a “do-it-yourself” (DIY) approach, empowering users to numerically simulate key macroeconomic models on their own using the open-source programming languages R and Python.  https://macrosimulation.org/
   ### A New Keynesian 3-Equation Model ###
    New Keynesian dynamic general equilibrium (DGE) models were developed during the 1990s and 2000s as tools for the analysis and conduct of monetary policy. These models build on the real business cycle framework with rational expectations, while incorporating Keynesian features such as imperfect competition and nominal rigidities. Although their structural representations are typically complex—since behavioural relationships are derived from agents’ intertemporal optimisation—the reduced form of the benchmark models can be summarised by three core equations: (i) an IS curve, (ii) a Phillips curve, and (iii) a monetary policy (interest rate) rule.

    The simplified three-equation model considered here is taken directly from Chapter 3 of Carlin and Soskice (2014). It is a short-run framework in which prices are flexible but the capital stock is fixed, so the emphasis is on goods market equilibrium rather than long-run growth. In the Carlin–Soskice formulation, inflation expectations are assumed to be adaptive, and aggregate demand responds gradually to changes in the interest rate. These features introduce dynamics into the model.
   
    #### Reference #### 
    [1]Carlin, Wendy, and David Soskice. 2014. Macroeconomics. Instititions, Instability, and the Financial System. Oxford University Press.
  
    [2]Galí, Jordi. 2018. “The State of New Keynesian Economics: A Partial Assessment.” Journal of Economic Perspectives 32 (3): 87–112. https://doi.org/10.1257/jep.32.3.87.

    [3]Free textbook in intermediate macroeconomics ( Free textbook for download ). https://www.stone-econ.org/resources/free-textbook-in-intermediate-macroeconomics

