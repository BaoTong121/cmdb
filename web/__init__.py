from cmdb.service import add_schema, add_field,get_schema_by_name
from flask import Flask, make_response, request, render_template, jsonify

app = Flask(__name__)


@app.route('/schema/creatschema', methods=['POST'])
def creatschema():
    try:
        schema = get_schema_by_name(request.json["schema_name"])
        if schema:
            return "已存在"
        add_schema(request.json["schema_name"], request.json.get("desc"))
        return "添加成功"
    except Exception as e:
        print(e)
@app.route('/schema/creatfield', methods=['POST'])
def creatfield():
    try:
        add_field(request.json['schema_name'], request.json['field_name'], request.json('mate'))
    except Exception as e:
        print(e)

