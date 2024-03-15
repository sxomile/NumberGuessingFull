# flake8: noqa
# fmt: off
# mypy: disable-error-code="no-any-return, no-untyped-call"
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^1.2.0
import base64
import dataclasses
import decimal
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.v2client import models
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AtomicTransactionResponse,
    SimulateAtomicTransactionResponse,
    TransactionSigner,
    TransactionWithSigner
)

_APP_SPEC_JSON = r"""{
    "hints": {
        "zapocni_igru()string": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "pogodi(pay,uint64)string": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "rezultat_igre()string": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "hello(string)string": {
            "call_config": {
                "no_op": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDAgMSAxMApieXRlY2Jsb2NrIDB4NzM2YjcyNjk3NjY1NmU2OTVmNjI3MjZmNmEgMHggMHg2MjcyNmY2YTYxNjMgMHgxNTFmN2M3NSAweDcyNjU3YTc1NmM3NDYxNzQKdHhuIE51bUFwcEFyZ3MKaW50Y18wIC8vIDAKPT0KYm56IG1haW5fbDEwCnR4bmEgQXBwbGljYXRpb25BcmdzIDAKcHVzaGJ5dGVzIDB4MDQxNGFmYjggLy8gInphcG9jbmlfaWdydSgpc3RyaW5nIgo9PQpibnogbWFpbl9sOQp0eG5hIEFwcGxpY2F0aW9uQXJncyAwCnB1c2hieXRlcyAweDVkZGQ1ZmNhIC8vICJwb2dvZGkocGF5LHVpbnQ2NClzdHJpbmciCj09CmJueiBtYWluX2w4CnR4bmEgQXBwbGljYXRpb25BcmdzIDAKcHVzaGJ5dGVzIDB4ZDg2MDA0MWUgLy8gInJlenVsdGF0X2lncmUoKXN0cmluZyIKPT0KYm56IG1haW5fbDcKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHgwMmJlY2UxMSAvLyAiaGVsbG8oc3RyaW5nKXN0cmluZyIKPT0KYm56IG1haW5fbDYKZXJyCm1haW5fbDY6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KJiYKYXNzZXJ0CmNhbGxzdWIgaGVsbG9jYXN0ZXJfMTEKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDc6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KJiYKYXNzZXJ0CmNhbGxzdWIgcmV6dWx0YXRpZ3JlY2FzdGVyXzEwCmludGNfMSAvLyAxCnJldHVybgptYWluX2w4Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CiYmCmFzc2VydApjYWxsc3ViIHBvZ29kaWNhc3Rlcl85CmludGNfMSAvLyAxCnJldHVybgptYWluX2w5Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CiYmCmFzc2VydApjYWxsc3ViIHphcG9jbmlpZ3J1Y2FzdGVyXzgKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDEwOgp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CmJueiBtYWluX2wxNAp0eG4gT25Db21wbGV0aW9uCmludGNfMSAvLyBPcHRJbgo9PQpibnogbWFpbl9sMTMKZXJyCm1haW5fbDEzOgp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQphc3NlcnQKY2FsbHN1YiBvcHRpbl8xCmludGNfMSAvLyAxCnJldHVybgptYWluX2wxNDoKdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKPT0KYXNzZXJ0CmNhbGxzdWIgY3JlYXRlXzAKaW50Y18xIC8vIDEKcmV0dXJuCgovLyBjcmVhdGUKY3JlYXRlXzA6CnByb3RvIDAgMApieXRlY18wIC8vICJza3JpdmVuaV9icm9qIgppbnRjXzAgLy8gMAphcHBfZ2xvYmFsX3B1dApyZXRzdWIKCi8vIG9wdF9pbgpvcHRpbl8xOgpwcm90byAwIDAKaW50Y18xIC8vIDEKcmV0dXJuCgovLyB6YXBvY25pX2lncnUKemFwb2NuaWlncnVfMjoKcHJvdG8gMCAxCmJ5dGVjXzEgLy8gIiIKYnl0ZWNfMCAvLyAic2tyaXZlbmlfYnJvaiIKcHVzaGludCA2IC8vIDYKYXBwX2dsb2JhbF9wdXQKcHVzaGJ5dGVzIDB4MDAzMTRlNjE2ZDY1NzM3NDY1NmUyMDZhNjUyMDczNmI3MjY5NzY2NTZlNjkyMDYyNzI2ZjZhMmUyMDUzNzI2NTYzNmU2ZjIwNzM2MTIwNzA2ZjY3NjE2NDZhNjE2ZTZhNjU2ZDIxIC8vIDB4MDAzMTRlNjE2ZDY1NzM3NDY1NmUyMDZhNjUyMDczNmI3MjY5NzY2NTZlNjkyMDYyNzI2ZjZhMmUyMDUzNzI2NTYzNmU2ZjIwNzM2MTIwNzA2ZjY3NjE2NDZhNjE2ZTZhNjU2ZDIxCmZyYW1lX2J1cnkgMApyZXRzdWIKCi8vIHBvZ29kaQpwb2dvZGlfMzoKcHJvdG8gMiAxCmJ5dGVjXzEgLy8gIiIKYnl0ZWNfMCAvLyAic2tyaXZlbmlfYnJvaiIKYXBwX2dsb2JhbF9nZXQKZnJhbWVfZGlnIC0xCj09CmJueiBwb2dvZGlfM19sMgp0eG4gU2VuZGVyCmJ5dGVjIDQgLy8gInJlenVsdGF0IgppbnRjXzAgLy8gMAphcHBfbG9jYWxfcHV0CmIgcG9nb2RpXzNfbDMKcG9nb2RpXzNfbDI6CnR4biBTZW5kZXIKZnJhbWVfZGlnIC0yCmd0eG5zIEFtb3VudApwdXNoaW50IDUgLy8gNQoqCmNhbGxzdWIgcGF5XzUKdHhuIFNlbmRlcgpieXRlYyA0IC8vICJyZXp1bHRhdCIKaW50Y18xIC8vIDEKYXBwX2xvY2FsX3B1dApjYWxsc3ViIHByb21lbmlicm9qXzYKcG9nb2RpXzNfbDM6CnJldHN1YgoKLy8gcmV6dWx0YXRfaWdyZQpyZXp1bHRhdGlncmVfNDoKcHJvdG8gMCAxCmJ5dGVjXzEgLy8gIiIKdHhuIFNlbmRlcgpieXRlYyA0IC8vICJyZXp1bHRhdCIKYXBwX2xvY2FsX2dldAppbnRjXzEgLy8gMQo9PQpibnogcmV6dWx0YXRpZ3JlXzRfbDIKcHVzaGJ5dGVzIDB4MDAxYzUwNzI2ZjZkNjE3MzYxNmEyMTIwNTA3MjZmNjI2MTZhMjA2NDcyNzU2NzY5MjA2MjcyNmY2YTJlIC8vIDB4MDAxYzUwNzI2ZjZkNjE3MzYxNmEyMTIwNTA3MjZmNjI2MTZhMjA2NDcyNzU2NzY5MjA2MjcyNmY2YTJlCmZyYW1lX2J1cnkgMApiIHJlenVsdGF0aWdyZV80X2wzCnJlenVsdGF0aWdyZV80X2wyOgpwdXNoYnl0ZXMgMHgwMDIzNTA2ZjY3NmY2NDYxNmIyMTIwNGU2Zjc2NjE2MzIwNmE2NTIwNzU3MDZjNjE2MzY1NmUyMDZlNjEyMDcyNjE2Mzc1NmUyZSAvLyAweDAwMjM1MDZmNjc2ZjY0NjE2YjIxMjA0ZTZmNzY2MTYzMjA2YTY1MjA3NTcwNmM2MTYzNjU2ZTIwNmU2MTIwNzI2MTYzNzU2ZTJlCmZyYW1lX2J1cnkgMApyZXp1bHRhdGlncmVfNF9sMzoKcmV0c3ViCgovLyBwYXkKcGF5XzU6CnByb3RvIDIgMAppdHhuX2JlZ2luCmludGNfMSAvLyBwYXkKaXR4bl9maWVsZCBUeXBlRW51bQpwdXNoaW50IDEwMDAgLy8gMTAwMAppdHhuX2ZpZWxkIEZlZQpmcmFtZV9kaWcgLTEKaXR4bl9maWVsZCBBbW91bnQKZnJhbWVfZGlnIC0yCml0eG5fZmllbGQgUmVjZWl2ZXIKaXR4bl9zdWJtaXQKcmV0c3ViCgovLyBwcm9tZW5pX2Jyb2oKcHJvbWVuaWJyb2pfNjoKcHJvdG8gMCAwCnR4biBTZW5kZXIKYnl0ZWNfMiAvLyAiYnJvamFjIgppbnRjXzAgLy8gMAphcHBfbG9jYWxfcHV0CnByb21lbmlicm9qXzZfbDE6CnR4biBTZW5kZXIKYnl0ZWNfMiAvLyAiYnJvamFjIgphcHBfbG9jYWxfZ2V0CnB1c2hpbnQgNyAvLyA3CjwKYm56IHByb21lbmlicm9qXzZfbDQKYnl0ZWNfMCAvLyAic2tyaXZlbmlfYnJvaiIKYXBwX2dsb2JhbF9nZXQKaW50Y18yIC8vIDEwCj4KYnogcHJvbWVuaWJyb2pfNl9sNQpieXRlY18wIC8vICJza3JpdmVuaV9icm9qIgpieXRlY18wIC8vICJza3JpdmVuaV9icm9qIgphcHBfZ2xvYmFsX2dldAppbnRjXzIgLy8gMTAKLQphcHBfZ2xvYmFsX3B1dApiIHByb21lbmlicm9qXzZfbDUKcHJvbWVuaWJyb2pfNl9sNDoKYnl0ZWNfMCAvLyAic2tyaXZlbmlfYnJvaiIKYnl0ZWNfMCAvLyAic2tyaXZlbmlfYnJvaiIKYXBwX2dsb2JhbF9nZXQKaW50Y18xIC8vIDEKKwphcHBfZ2xvYmFsX3B1dAp0eG4gU2VuZGVyCmJ5dGVjXzIgLy8gImJyb2phYyIKdHhuIFNlbmRlcgpieXRlY18yIC8vICJicm9qYWMiCmFwcF9sb2NhbF9nZXQKaW50Y18xIC8vIDEKKwphcHBfbG9jYWxfcHV0CmIgcHJvbWVuaWJyb2pfNl9sMQpwcm9tZW5pYnJval82X2w1Ogp0eG4gU2VuZGVyCmJ5dGVjXzIgLy8gImJyb2phYyIKaW50Y18wIC8vIDAKYXBwX2xvY2FsX3B1dApyZXRzdWIKCi8vIGhlbGxvCmhlbGxvXzc6CnByb3RvIDEgMQpieXRlY18xIC8vICIiCnB1c2hieXRlcyAweDQ4NjU2YzZjNmYyYzIwIC8vICJIZWxsbywgIgpmcmFtZV9kaWcgLTEKZXh0cmFjdCAyIDAKY29uY2F0CmZyYW1lX2J1cnkgMApmcmFtZV9kaWcgMApsZW4KaXRvYgpleHRyYWN0IDYgMApmcmFtZV9kaWcgMApjb25jYXQKZnJhbWVfYnVyeSAwCnJldHN1YgoKLy8gemFwb2NuaV9pZ3J1X2Nhc3Rlcgp6YXBvY25paWdydWNhc3Rlcl84Ogpwcm90byAwIDAKYnl0ZWNfMSAvLyAiIgpjYWxsc3ViIHphcG9jbmlpZ3J1XzIKZnJhbWVfYnVyeSAwCmJ5dGVjXzMgLy8gMHgxNTFmN2M3NQpmcmFtZV9kaWcgMApjb25jYXQKbG9nCnJldHN1YgoKLy8gcG9nb2RpX2Nhc3Rlcgpwb2dvZGljYXN0ZXJfOToKcHJvdG8gMCAwCmJ5dGVjXzEgLy8gIiIKaW50Y18wIC8vIDAKZHVwCnR4bmEgQXBwbGljYXRpb25BcmdzIDEKYnRvaQpmcmFtZV9idXJ5IDIKdHhuIEdyb3VwSW5kZXgKaW50Y18xIC8vIDEKLQpmcmFtZV9idXJ5IDEKZnJhbWVfZGlnIDEKZ3R4bnMgVHlwZUVudW0KaW50Y18xIC8vIHBheQo9PQphc3NlcnQKZnJhbWVfZGlnIDEKZnJhbWVfZGlnIDIKY2FsbHN1YiBwb2dvZGlfMwpmcmFtZV9idXJ5IDAKYnl0ZWNfMyAvLyAweDE1MWY3Yzc1CmZyYW1lX2RpZyAwCmNvbmNhdApsb2cKcmV0c3ViCgovLyByZXp1bHRhdF9pZ3JlX2Nhc3RlcgpyZXp1bHRhdGlncmVjYXN0ZXJfMTA6CnByb3RvIDAgMApieXRlY18xIC8vICIiCmNhbGxzdWIgcmV6dWx0YXRpZ3JlXzQKZnJhbWVfYnVyeSAwCmJ5dGVjXzMgLy8gMHgxNTFmN2M3NQpmcmFtZV9kaWcgMApjb25jYXQKbG9nCnJldHN1YgoKLy8gaGVsbG9fY2FzdGVyCmhlbGxvY2FzdGVyXzExOgpwcm90byAwIDAKYnl0ZWNfMSAvLyAiIgpkdXAKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQpmcmFtZV9idXJ5IDEKZnJhbWVfZGlnIDEKY2FsbHN1YiBoZWxsb183CmZyYW1lX2J1cnkgMApieXRlY18zIC8vIDB4MTUxZjdjNzUKZnJhbWVfZGlnIDAKY29uY2F0CmxvZwpyZXRzdWI=",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDgKcHVzaGludCAwIC8vIDAKcmV0dXJu"
    },
    "state": {
        "global": {
            "num_byte_slices": 0,
            "num_uints": 1
        },
        "local": {
            "num_byte_slices": 0,
            "num_uints": 2
        }
    },
    "schema": {
        "global": {
            "declared": {
                "skriveni_broj": {
                    "type": "uint64",
                    "key": "skriveni_broj",
                    "descr": ""
                }
            },
            "reserved": {}
        },
        "local": {
            "declared": {
                "brojac": {
                    "type": "uint64",
                    "key": "brojac",
                    "descr": ""
                },
                "rezultat": {
                    "type": "uint64",
                    "key": "rezultat",
                    "descr": ""
                }
            },
            "reserved": {}
        }
    },
    "contract": {
        "name": "Pogadjanje",
        "methods": [
            {
                "name": "zapocni_igru",
                "args": [],
                "returns": {
                    "type": "string"
                }
            },
            {
                "name": "pogodi",
                "args": [
                    {
                        "type": "pay",
                        "name": "uplata"
                    },
                    {
                        "type": "uint64",
                        "name": "broj"
                    }
                ],
                "returns": {
                    "type": "string"
                }
            },
            {
                "name": "rezultat_igre",
                "args": [],
                "returns": {
                    "type": "string"
                }
            },
            {
                "name": "hello",
                "args": [
                    {
                        "type": "string",
                        "name": "name"
                    }
                ],
                "returns": {
                    "type": "string"
                }
            }
        ],
        "networks": {}
    },
    "bare_call_config": {
        "no_op": "CREATE",
        "opt_in": "CALL"
    }
}"""
APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase[typing.Any])


@dataclasses.dataclass(kw_only=True)
class _TArgsHolder(typing.Generic[_TArgs]):
    args: _TArgs


def _filter_none(value: dict | typing.Any) -> dict | typing.Any:
    if isinstance(value, dict):
        return {k: _filter_none(v) for k, v in value.items() if v is not None}
    return value


def _as_dict(data: typing.Any, *, convert_all: bool = True) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    if convert_all:
        result = dataclasses.asdict(data)
    else:
        result = {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}
    return _filter_none(result)


def _convert_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.TransactionParametersDict:
    return typing.cast(algokit_utils.TransactionParametersDict, _as_dict(transaction_parameters))


def _convert_call_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.OnCompleteCallParametersDict:
    return typing.cast(algokit_utils.OnCompleteCallParametersDict, _as_dict(transaction_parameters))


def _convert_create_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
    on_complete: algokit_utils.OnCompleteActionName,
) -> algokit_utils.CreateCallParametersDict:
    result = typing.cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    result["on_complete"] = getattr(algosdk.transaction.OnComplete, on_complete_enum)
    return result


def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> algokit_utils.ABICreateCallArgsDict | None:
    if deploy_args is None:
        return None

    deploy_args_dict = typing.cast(algokit_utils.ABICreateCallArgsDict, _as_dict(deploy_args))
    if isinstance(deploy_args, _TArgsHolder):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict


@dataclasses.dataclass(kw_only=True)
class ZapocniIgruArgs(_ArgsBase[str]):
    @staticmethod
    def method() -> str:
        return "zapocni_igru()string"


@dataclasses.dataclass(kw_only=True)
class PogodiArgs(_ArgsBase[str]):
    uplata: TransactionWithSigner
    broj: int

    @staticmethod
    def method() -> str:
        return "pogodi(pay,uint64)string"


@dataclasses.dataclass(kw_only=True)
class RezultatIgreArgs(_ArgsBase[str]):
    @staticmethod
    def method() -> str:
        return "rezultat_igre()string"


@dataclasses.dataclass(kw_only=True)
class HelloArgs(_ArgsBase[str]):
    name: str

    @staticmethod
    def method() -> str:
        return "hello(string)string"


class GlobalState:
    def __init__(self, data: dict[bytes, bytes | int]):
        self.skriveni_broj = typing.cast(int, data.get(b"skriveni_broj"))


class LocalState:
    def __init__(self, data: dict[bytes, bytes | int]):
        self.brojac = typing.cast(int, data.get(b"brojac"))
        self.rezultat = typing.cast(int, data.get(b"rezultat"))


@dataclasses.dataclass(kw_only=True)
class SimulateOptions:
    allow_more_logs: bool = dataclasses.field(default=False)
    allow_empty_signatures: bool = dataclasses.field(default=False)
    extra_opcode_budget: int = dataclasses.field(default=0)
    exec_trace_config: models.SimulateTraceConfig | None         = dataclasses.field(default=None)


class Composer:

    def __init__(self, app_client: algokit_utils.ApplicationClient, atc: AtomicTransactionComposer):
        self.app_client = app_client
        self.atc = atc

    def build(self) -> AtomicTransactionComposer:
        return self.atc

    def simulate(self, options: SimulateOptions | None = None) -> SimulateAtomicTransactionResponse:
        request = models.SimulateRequest(
            allow_more_logs=options.allow_more_logs,
            allow_empty_signatures=options.allow_empty_signatures,
            extra_opcode_budget=options.extra_opcode_budget,
            exec_trace_config=options.exec_trace_config,
            txn_groups=[]
        ) if options else None
        result = self.atc.simulate(self.app_client.algod_client, request)
        return result

    def execute(self) -> AtomicTransactionResponse:
        return self.app_client.execute_atc(self.atc)

    def zapocni_igru(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `zapocni_igru()string` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = ZapocniIgruArgs()
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def pogodi(
        self,
        *,
        uplata: TransactionWithSigner,
        broj: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `pogodi(pay,uint64)string` ABI method
        
        :param TransactionWithSigner uplata: The `uplata` ABI parameter
        :param int broj: The `broj` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = PogodiArgs(
            uplata=uplata,
            broj=broj,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def rezultat_igre(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `rezultat_igre()string` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = RezultatIgreArgs()
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def hello(
        self,
        *,
        name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `hello(string)string` ABI method
        
        :param str name: The `name` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = HelloArgs(
            name=name,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to create an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_create(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return self

    def opt_in_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a calls to the opt_in bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_opt_in(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return self

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> "Composer":
        """Adds a call to the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass"""
    
        self.app_client.compose_clear_state(self.atc, _convert_transaction_parameters(transaction_parameters), app_args)
        return self


class PogadjanjeClient:
    """A class for interacting with the Pogadjanje app providing high productivity and
    strongly typed methods to deploy and call the app"""

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        """
        PogadjanjeClient can be created with an app_id to interact with an existing application, alternatively
        it can be created with a creator and indexer_client specified to find existing applications by name and creator.
        
        :param AlgodClient algod_client: AlgoSDK algod client
        :param int app_id: The app_id of an existing application, to instead find the application by creator and name
        use the creator and indexer_client parameters
        :param str | Account creator: The address or Account of the app creator to resolve the app_id
        :param IndexerClient indexer_client: AlgoSDK indexer client, only required if deploying or finding app_id by
        creator and app name
        :param AppLookup existing_deployments:
        :param TransactionSigner | Account signer: Account or signer to use to sign transactions, if not specified and
        creator was passed as an Account will use that.
        :param str sender: Address to use as the sender for all transactions, will use the address associated with the
        signer if not specified.
        :param TemplateValueMapping template_values: Values to use for TMPL_* template variables, dictionary keys should
        *NOT* include the TMPL_ prefix
        :param str | None app_name: Name of application to use when deploying, defaults to name defined on the
        Application Specification
            """

        self.app_spec = APP_SPEC
        
        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
            app_name=app_name,
        )

    @property
    def algod_client(self) -> algosdk.v2client.algod.AlgodClient:
        return self.app_client.algod_client

    @property
    def app_id(self) -> int:
        return self.app_client.app_id

    @app_id.setter
    def app_id(self, value: int) -> None:
        self.app_client.app_id = value

    @property
    def app_address(self) -> str:
        return self.app_client.app_address

    @property
    def sender(self) -> str | None:
        return self.app_client.sender

    @sender.setter
    def sender(self, value: str) -> None:
        self.app_client.sender = value

    @property
    def signer(self) -> TransactionSigner | None:
        return self.app_client.signer

    @signer.setter
    def signer(self, value: TransactionSigner) -> None:
        self.app_client.signer = value

    @property
    def suggested_params(self) -> algosdk.transaction.SuggestedParams | None:
        return self.app_client.suggested_params

    @suggested_params.setter
    def suggested_params(self, value: algosdk.transaction.SuggestedParams | None) -> None:
        self.app_client.suggested_params = value

    def get_global_state(self) -> GlobalState:
        """Returns the application's global state wrapped in a strongly typed class with options to format the stored value"""

        state = typing.cast(dict[bytes, bytes | int], self.app_client.get_global_state(raw=True))
        return GlobalState(state)

    def get_local_state(self, account: str | None = None) -> LocalState:
        """Returns the application's local state wrapped in a strongly typed class with options to format the stored value"""

        state = typing.cast(dict[bytes, bytes | int], self.app_client.get_local_state(account, raw=True))
        return LocalState(state)

    def zapocni_igru(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Calls `zapocni_igru()string` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[str]: The result of the transaction"""

        args = ZapocniIgruArgs()
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def pogodi(
        self,
        *,
        uplata: TransactionWithSigner,
        broj: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Calls `pogodi(pay,uint64)string` ABI method
        
        :param TransactionWithSigner uplata: The `uplata` ABI parameter
        :param int broj: The `broj` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[str]: The result of the transaction"""

        args = PogodiArgs(
            uplata=uplata,
            broj=broj,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def rezultat_igre(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Calls `rezultat_igre()string` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[str]: The result of the transaction"""

        args = RezultatIgreArgs()
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def hello(
        self,
        *,
        name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Calls `hello(string)string` ABI method
        
        :param str name: The `name` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[str]: The result of the transaction"""

        args = HelloArgs(
            name=name,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Creates an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.create(
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return result

    def opt_in_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the opt_in bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.opt_in(
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return result

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass
        :returns algokit_utils.TransactionResponse: The result of the transaction"""
    
        return self.app_client.clear_state(_convert_transaction_parameters(transaction_parameters), app_args)

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: algokit_utils.DeployCallArgs | None = None,
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: algokit_utils.DeployCallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        """Deploy an application and update client to reference it.
        
        Idempotently deploy (create, update/delete if changed) an app against the given name via the given creator
        account, including deploy-time template placeholder substitutions.
        To understand the architecture decisions behind this functionality please see
        <https://github.com/algorandfoundation/algokit-cli/blob/main/docs/architecture-decisions/2023-01-12_smart-contract-deployment.md>
        
        ```{note}
        If there is a breaking state schema change to an existing app (and `on_schema_break` is set to
        'ReplaceApp' the existing app will be deleted and re-created.
        ```
        
        ```{note}
        If there is an update (different TEAL code) to an existing app (and `on_update` is set to 'ReplaceApp')
        the existing app will be deleted and re-created.
        ```
        
        :param str version: version to use when creating or updating app, if None version will be auto incremented
        :param algosdk.atomic_transaction_composer.TransactionSigner signer: signer to use when deploying app
        , if None uses self.signer
        :param str sender: sender address to use when deploying app, if None uses self.sender
        :param bool allow_delete: Used to set the `TMPL_DELETABLE` template variable to conditionally control if an app
        can be deleted
        :param bool allow_update: Used to set the `TMPL_UPDATABLE` template variable to conditionally control if an app
        can be updated
        :param OnUpdate on_update: Determines what action to take if an application update is required
        :param OnSchemaBreak on_schema_break: Determines what action to take if an application schema requirements
        has increased beyond the current allocation
        :param dict[str, int|str|bytes] template_values: Values to use for `TMPL_*` template variables, dictionary keys
        should *NOT* include the TMPL_ prefix
        :param algokit_utils.DeployCallArgs | None create_args: Arguments used when creating an application
        :param algokit_utils.DeployCallArgs | None update_args: Arguments used when updating an application
        :param algokit_utils.DeployCallArgs | None delete_args: Arguments used when deleting an application
        :return DeployResponse: details action taken and relevant transactions
        :raises DeploymentError: If the deployment failed"""

        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=_convert_deploy_args(create_args),
            update_args=_convert_deploy_args(update_args),
            delete_args=_convert_deploy_args(delete_args),
        )

    def compose(self, atc: AtomicTransactionComposer | None = None) -> Composer:
        return Composer(self.app_client, atc or AtomicTransactionComposer())
