import sys
import logging
from argparse import ArgumentParser
from historical.app import App

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

argparser = ArgumentParser(
    prog='StockHist',
    description='Histórico de ações on your terminal')

required = argparser.add_argument_group('argumentos requeridos')

required.add_argument('-a', '--acao',
                      required=True,
                      dest='stock_code',
                      help=('Código da ação para consulta'))

argparser.add_argument('-v', '--version',
                       action='version',
                       version='%(prog)s 1.0')


args = argparser.parse_args()

app = App(args.stock_code)
app.run()