from flask import Flask, render_template, request
import spider
import sys

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    query = request.args.get('q')
    if request.method == 'GET' and query:

        # query = "XP Investimentos"
        # print(query)
        # sys.exit(1)

        estadao = spider.Spider()
        estadao.query = query

        valor = spider.Spider()
        valor.query = query

        folhasp = spider.Spider()
        folhasp.query = query

        o_globo = spider.Spider()
        o_globo.query = query

        valor_investe = spider.Spider()
        valor_investe.query = query

        einvestidor = spider.Spider()
        einvestidor.query = query

        pipeline = spider.Spider()
        pipeline.query = query

        neofeed = spider.Spider()
        neofeed.query = query

        braziljournal = spider.Spider()
        braziljournal.query = query

        return render_template('search-result.html',
                               valor_data=valor.getValor(),
                               estadao_data=estadao.getEstadao(),
                               folhasp_data=folhasp.getFolhaSP(),
                               o_globo_data=o_globo.getOGlobo(),
                               valor_investe=valor_investe.getValorInveste(),
                               # einvestidor=einvestidor.getEInvestidor(),
                               pipeline=pipeline.getPipeline(),
                               neofeed=neofeed.getNeofeed(),
                               braziljournal=braziljournal.getBrazilJournal()
                               )
    else:
        return render_template('index.html')
