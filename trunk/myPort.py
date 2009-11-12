#!/usr/local/bin/python
#
# 'borrowed' from the sample code
# /usr/local/src/google/gdata-2.0.0/samples/finance
#

__author__ = 'Geoff@GeoffLamb.com'


from gdata.finance.service import \
    FinanceService, PortfolioQuery, PositionQuery
from gdata.finance import \
    PortfolioEntry, PortfolioData, TransactionEntry, TransactionData, \
    Price, Commission, Money
import datetime
import sys
# http://www.goldb.org/ystockquote.html
import ystockquote

def PrintPosition(pos, with_returns=False):
  """Print single position."""
  print pos.ticker_id.split(":")[1].ljust(5),
  d = pos.position_data
  print d.shares.rjust(5),
  #print "%1.2f" % float(((d.gain_percentage) * 100)),
  #print "%1.2f" % ((float(d.gain_percentage) * 100)),
  print (d.cost_basis.money[0].amount).rjust(10),
  print "%0.2f" % float(d.days_gain.money[0].amount),
  print "%1.2f" % float(d.gain.money[0].amount),
  print "%2.2f" % float(d.market_value.money[0].amount)

def PrintTickerDetails(tick, with_returns=False):
  """Print single ticker."""
  code =  tick + '.AX'
  dict = ystockquote.get_all(code)
  print tick,
  print "%1.2f" % (float(dict['price'])),
  print dict['change'],
  print dict['volume'],
  print dict['avg_daily_volume'],
  print dict['52_week_high'],
  print dict['52_week_low'],
  print dict['50day_moving_avg'],
  print dict['200day_moving_avg']

class myPorts(object):

  def __init__(self, email, password):
    self.client = FinanceService(source='myPort')
    self.client.ClientLogin(email, password)
  
  def GetPortfolios(self, with_returns=False, inline_positions=False): 
    query = PortfolioQuery()
    query.returns = with_returns
    query.positions = inline_positions
    return self.client.GetPortfolioFeed(query=query).entry

  def GetPositions(self, portfolio, with_returns=False, inline_transactions=False):
    query = PositionQuery()
    query.returns = with_returns
    query.transactions = inline_transactions
    return self.client.GetPositionFeed(portfolio, query=query).entry

  def ShowDetails(self, with_returns=False, inline_positions=False,
      inline_transactions=False):
    portfolios = self.GetPortfolios(with_returns, inline_positions)
    for pfl in portfolios:
      positions = self.GetPositions(pfl, with_returns, inline_transactions)
      print '================================================================================'
      print 'Ticker Shares Gain%  Cost  Days Gain Market Value'
      print '================================================================================'
      for pos in positions:
        PrintPosition(pos, with_returns)
      print '================================================================================'

  def ShowTickerDetails(self, with_returns=False, inline_positions=False,
      inline_transactions=False):
    portfolios = self.GetPortfolios(with_returns, inline_positions)
    for pfl in portfolios:
      positions = self.GetPositions(pfl, with_returns, inline_transactions)
      print ''
      print '================================================================================'
      print 'Ticker price change volume avg_daily_volume 52_week_high 52_week_low 50day_moving_avg 200day_moving_avg'

      print '================================================================================'
      for pos in positions:
        tick = pos.ticker_id.split(":")[1]
        PrintTickerDetails(tick, with_returns)
      print '================================================================================'
      print ''


  def GetPosition(self, portfolio, ticker, with_returns=False, inline_transactions=False):
    query = PositionQuery()
    query.returns = with_returns
    query.transactions = inline_transactions
    return self.client.GetPosition(
        portfolio_id=portfolio.portfolio_id, ticker_id=ticker, query=query)

if __name__ == '__main__':
  try:
    email = sys.argv[1]
    password = sys.argv[2]
    cases = sys.argv[3:]
  except IndexError:
    print "Usage: myPort.py account@google.com password [0 1 2...]"
    sys.exit(1)

  getPort = myPorts(email, password)
  #getPort.ShowTickerDetails(with_returns=True)
  getPort.ShowDetails(with_returns=True)
