import ujson
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
from uc_http_requester.requester import Request


class NodeType(flow.NodeType):
    id: str = '80eadd09-3f33-4148-80ee-adde09856abf'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'lexal_name'
    is_public: bool = False
    displayName: str = 'lexal_display'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'lexal_description'
    properties: List[Property] = [
        Property(
            displayName='Текстовое поле',
            name='str_field',
            type=Property.Type.STRING,
            placeholder='',
            description='number',
            required=True,
            default="0",
        ),
        Property(
            displayName='Числовое поле',
            name='int_field',
            type=Property.Type.NUMBER,
            placeholder='',
            description='number',
            required=True,
            default=0,
        ),
        Property(
            displayName='Переключатель в строку',
            name='change_field',
            type=Property.Type.BOOLEAN,
            description='Выключено -> int; Включено -> str',
            required=True,
            default=False,
        )
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            try:
                str_field = int(json.node.data.properties['str_field'])
            except ValueError:
                raise ValueError('Должны быть введены цифры в текстовое поле!')
            result = str_field + json.node.data.properties['int_field']
            if json.node.data.properties['change_field']:
                result = str(result)
            await json.save_result({
                "result": result
            })
            json.state = RunState.complete
        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error
        return json


class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = InfoView
        Execute = ExecuteView
