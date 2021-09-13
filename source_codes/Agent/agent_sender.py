from flask import Flask, jsonify # importing the Flask class from flask library
import agent_collector as collector


app = Flask(__name__)    # initiating the Flask app object 
app.config['JSON_SORT_KEYS'] = False #disables auto ordering keys


@app.route("/")    #creating endpoint
def hello():       #method for the associated endpoint 
    return 'hello world'

@app.route("/node_util/<resource>")    #creating endpoint
def call_collector(resource):     
    if resource.lower() ==  'all':
        return jsonify(
                collector.run_util_collection(exit_iface='Wi-Fi')
        )
    elif resource.lower() == 'cpu':
        return jsonify(
                collector.run_util_collection(exit_iface='Wi-Fi')['node_util']['cpu']
        )
    elif resource.lower() == 'memory':
        return jsonify(
                collector.run_util_collection(exit_iface='Wi-Fi')['node_util']['memory']
        )
    elif resource.lower() == 'network':
        return jsonify(
                collector.run_util_collection(exit_iface='Wi-Fi')['node_util']['network']
        )
    else:
         return jsonify(
                {'message': 'Error : Unexpected key requested (use cpu/memory/network)'}
        )
if __name__ == '__main__':
    app.run(debug=True)