try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys
    sys.exit(1)

import asyncio
from datetime import datetime
from ocpp.routing import on
from ocpp.routing import after
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus, AuthorizationStatus, ClearCacheStatus, RemoteStartStopStatus,\
    DataTransferStatus, ChargingProfilePurposeType,ChargingProfileKindType, RecurrencyKind, ChargingRateUnitType,\
    AvailabilityType,UpdateType,ResetType
from ocpp.v16 import call_result
from ocpp.v16 import call

import json
import os

class ChargePoint(cp):                     # chargePoint 类
    '''
    @on(Action.BootNotification)
    def on_boot_notification(charge_point_model, charge_point_vendor, **kwargs):  # noqa
        print(f'{charge_point_model} from {charge_point_vendor} has booted.')  # noqa
        return call_result(BootNotificationPayload(
            current_time=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') + "Z",  # noqa
            interval=30,
            status="Accepted",
        )
    '''


    # export json file
    '''
    if does not exist, create automatically
    add local_time in output json data
    add function name in output json data
    
    two data folder:
    1.dataFromCp2Server:  initial form client, (req, con)
    2.dataFromServer2Cp:  initial form server, (req, con)
    '''
    def export_json_file(self, data, dir_path, function_name):
        # path = "./dataFromCp"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        else:
            pass

        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        data["local_time"] = current_time
        data["function_name"] = function_name

        jsondata = json.dumps(data, indent=4, separators=(',', ': '))
        with open(f'{dir_path}/{function_name}{current_time}.json', 'w') as f:
            f.write(jsondata)

    # 1
    @on(Action.BootNotification)           #  BootNotification 函数
    def on_boot_notification(self, **kwargs):
        print("cp -> server , on_boot_notification: \n", kwargs, "\n")
        self.export_json_file(kwargs, "./dataFromCp2Server", "BootNotification.req")

        response = call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

        self.export_json_file(response.__dict__, "./dataFromCp2Server", "BootNotification.con")
        print("server -> cp, on_boot_notification: \n", response, "\n")
        return response

    #     return call_result.BootNotificationPayload(
    #         current_time=datetime.utcnow().isoformat(),
    #         interval=10,
    #         status=RegistrationStatus.accepted
    # )

    # 2
    @on(Action.Authorize)  #
    def on_authorize_notification(self, **kwargs):
        print("cp -> server , on_authorize_notification: \n", kwargs, "\n")
        self.export_json_file(kwargs, "./dataFromCp2Server","Authorize.req")

        response = call_result.AuthorizePayload(
            id_tag_info={'expiryDate': datetime.utcnow().isoformat(),
                         'parentIdTag': '123hhh',                  # Optional. This contains the parent-identifier.
                         'status': AuthorizationStatus.accepted    # Required. This contains whether the idTag has been accepted or not by the Central System.
                         }
        )
        self.export_json_file(response.__dict__, "./dataFromCp2Server", "Authorize.con")
        print("server -> cp, on_authorize_notification: \n", response, "\n")
        return response


    # 3
    @on(Action.Heartbeat)  #
    def on_heartbeat_notification(self, **kwargs):
        print("on heart beat is", kwargs)
        # self.export_json_file(kwargs, "./dataFromCp2Server", "Heartbeat.req")

        response= call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat()
        )
        # self.export_json_file(response.__dict__, "./dataFromCp2Server", "Heartbeat.con")
        return response


    # 4
    @on(Action.StartTransaction)  #
    def on_start_transaction_notification(self, **kwargs):
        print("cp -> server , on_start_transaction_notification: \n", kwargs, "\n")
        self.export_json_file(kwargs, "./dataFromCp2Server", "StartTransaction.req")

        response = call_result.StartTransactionPayload(
            transaction_id=11111,  # Required. This contains the transaction id supplied by the Central System.
            id_tag_info={'expiryDate': datetime.now().isoformat(),  #Required. This contains information about authorization status, expiry and parent id.
                         'parentIdTag': '123hhh',
                         'status': AuthorizationStatus.accepted}
        )
        self.export_json_file(response.__dict__, "./dataFromCp2Server", "StartTransaction.con")
        print("server -> cp, on_start_transaction_notification: \n", response, "\n")

        return response

    @after(Action.StartTransaction)
    async def after_start_transaction(self, **kwargs):
        # print("after_start_transaction is ", kwargs)
        # self.export_json_file(kwargs, "./dataFromServer2CP", "StartTransaction")
        # await self.set_charging_profile(limit=100)
        await self.set_charging_profile(limit=100)
    #


    # 5
    @on(Action.StopTransaction)  #
    def on_stop_transaction_notification(self, **kwargs):
        print("cp -> server , on_stop_transaction_notification: \n", kwargs, "\n")
        self.export_json_file(kwargs, "./dataFromCp2Server", "StopTransaction.req")

        response = call_result.StopTransactionPayload(

            id_tag_info={'expiryDate': datetime.utcnow().isoformat(),
                         'parentIdTag': '123hhh',
                         'status': AuthorizationStatus.accepted}
        )

        self.export_json_file(response.__dict__, "./dataFromCp2Server", "StopTransaction.con")
        print("server -> cp, on_stop_transaction_notification: \n", response, "\n")
        return response

    # 6
    @on(Action.MeterValues)  #
    def on_meter_values_notification(self, **kwargs):
        print("cp -> server , on_meter_values_notification: \n", kwargs, "\n")
        self.export_json_file(kwargs, "./dataFromCp2Server", "MeterValues.req")

        response = call_result.MeterValuesPayload(
        )
        self.export_json_file(response.__dict__, "./dataFromCp2Server", "MeterValues.con")
        print("server -> cp, on_meter_values_notification: \n", response, "\n")
        return response

    # 7
    @on(Action.StatusNotification)  #
    def on_status_notification(self, **kwargs):
        print("cp -> server , on_status_notification: \n", kwargs, "\n")
        self.export_json_file(kwargs, "./dataFromCp2Server", "StatusNotification.req")

        response = call_result.StatusNotificationPayload(
        )
        self.export_json_file(response.__dict__, "./dataFromCp2Server", "StatusNotification.con")
        print("server -> cp, on_status_notification: \n", response, "\n")
        return response


    # 8   from GUI / special cp
    @on(Action.DataTransfer)
    async def on_data_transfer_notification(self, **kwargs):
        self.export_json_file(kwargs, "./dataFromCp2Server", "DataTransfer.req")
        print("cp -> server , on_data_transfer_notification: \n", kwargs, "\n")

        vendor_id = kwargs["vendor_id"]
        # print(vendor_id)
        message_id = kwargs["message_id"]
        # print(message_id)
        data = kwargs["data"]               # data type is <class 'str'>
        # print("data type is", type(data))
        # print("data is", data)


        # data_dict = json.dumps(data)           # json str to dict
        # print("======================")
        # data_dict = eval(data)
        # import ast
        # data_dict = ast.literal_eval(data)
        # import requests
        data_dict = json.loads(data)           #  <class 'dict'>
        # print(type(data_dict))
        # print("data_dict is", data_dict)

        # print(data_dict["cp_id"])
        # print(data_dict)
        # print(data_dict["connectorId"])
        # print(data_dict["authData"])

        if vendor_id == "MOEV_GUI":
            print("EVSE_dict is ", EVSE_dict)
            # get the cp instance
            if data_dict.get("cp_id"):
                cp_id = data_dict["cp_id"]
                # print("cp_id from GUI is", cp_id)
                cp_select = EVSE_dict[cp_id]
                # print("cp_select is", cp_select)
            if data_dict.get("max_watts"):
                max_watts = data_dict["max_watts"]
                # print("max_watts is", max_watts)
            if data_dict.get("max_current"):
                max_current = data_dict["max_current"]
                # print("max_current is", max_current)

            # cp_select = EVSE_dict[cp_id]
            # print("cp_select is", cp_select)

            ######## different command different function
            if message_id == "show current evses":
                response = call_result.DataTransferPayload(
                    status=DataTransferStatus.accepted,
                    data=str(EVSE_dict.keys())
                )
                self.export_json_file(response.__dict__, "./dataFromCp2Server", "DataTransfer.con")
                print("server -> gui, on_data_transfer_notification: \n", response, "\n")
                return response

            elif message_id == "start remote transaction":
                print("server - before remote start transaction")

                await cp_select.send_remote_start_transaction()

                response = call_result.DataTransferPayload(
                    status=DataTransferStatus.accepted,
                    data="we accepted the start remote transaction request, the evse is: %s" % cp_id
                )
                self.export_json_file(response.__dict__, "./dataFromCp2Server", "DataTransfer.con")
                print("server -> gui, on_data_transfer_notification: \n", response, "\n")
                return response

            elif message_id == "stop remote transaction":
                await cp_select.send_remote_stop_transaction()

                response = call_result.DataTransferPayload(
                    status=DataTransferStatus.accepted,
                    data="we accepted the stop remote transaction request, the evse is: %s" % cp_id
                )
                self.export_json_file(response.__dict__, "./dataFromCp2Server", "DataTransfer.con")
                print("server -> gui, on_data_transfer_notification: \n", response, "\n")
                return response

            elif message_id == "clear charging profile":
                await cp_select.clear_charging_profile()

                response = call_result.DataTransferPayload(
                    status=DataTransferStatus.accepted,
                    data="we accepted the clear charging profile request"
                )
                self.export_json_file(response.__dict__, "./dataFromCp2Server", "DataTransfer.con")
                print("server -> gui, on_data_transfer_notification: \n", response, "\n")
                return response

            elif message_id == "change max_watts":
                limit = max_watts

                await cp_select.set_charging_profile(limit)

                response = call_result.DataTransferPayload(
                    status=DataTransferStatus.accepted,
                    data="we accepted the change max watts request"
                )
                self.export_json_file(response.__dict__, "./dataFromCp2Server", "DataTransfer.con")
                print("server -> gui, on_data_transfer_notification: \n", response, "\n")
                return response

        elif vendor_id == "< EVSE_MANUFACTURER >":

            if message_id =="AuthorizedPayment.req":
                connector_id = data_dict["connectorId"]
                print(connector_id)
                pay_session_id = data_dict["paySessionId"]
                print(pay_session_id)
                auth_data_all = data_dict["authData"]
                print(auth_data_all)
                timestamp = data_dict["timestamp"]
                print(timestamp)

                ## for every auth_data in auth_data:
                auth_data = auth_data_all[0]
                payment_type = auth_data["Payment Type"]
                ccdata = auth_data["CCDATA"]
                decrypted_data_len = auth_data["decryptedDataLen"]
                ksn = auth_data["KSN"]
                # this vendorid is same with the previous one ??
                vendor_id = auth_data["vendorId"]
                print(vendor_id)
                version = auth_data["version"]
                phone = auth_data["phone"]
                email = auth_data["email"]
                price_code = auth_data["priceCode"]

                response = call_result.DataTransferPayload(
                    status=DataTransferStatus.accepted,
                    data=str({"status": "CreditCardAuthorizationStatus"})
                )
                print("server->cp , AuthorizedPayment \n", response, "\n")
                return response

                # await cp_select.authorized_payment()

            if message_id =="FetchImageInfo.req":
                data={}
#                 data = {"imageLang":[{"lang":"en_US",
#                                       "imageScreen":[{"screenId":"SCREEN_SAVER",
#                                                       "imageSection":[{"sectionName":"FULL_SCREEN",
#                                                                        "imageData":[{"duration":30,
#                                                                                      "url":"http://www.btcpower.com/assets/images/work/EV_Fast_Charger.png",
#                                                                                      "order":1,
#                                                                                      "resolution":"1032 * 706"}]},
#                                                                        {"sectionName":"FULL_SCREEN",
#                                                                         "imageData":[{"duration":30,
#                                                                                       "url":"http://www.btcpower.com/assets/images/work/EV_Fast_Charger.png",
#                                                                                       "order":2,
#                                                                                       "resolution":"1032 * 706"}]}]},
#                                                      {"screenId":"CHARGING_SCREEN",
#                                                       "imageSection":[{"sectionName":"ADVERTISEMENT",
#                                                                        "imageData":[{[{"duration": 30,
#                                                                                        "url":"http://www.btcpower.com/assets/images/work/EV_Fast_Charger.png",
#                                                                                        "order": 1,
#                                                                                        "resolution":"990 *220"}]}]},
#                                                                       {}]}]
#                 },{\\"screenId \\":":\\"PRICING_SCREEN \\",",\\"imageSection ":[{":[{\\"sectionName \\":":\\"FULL_SCREEN \\",",\\"imageData \\":[{":[{\\"duration \\": 30,\\"url \\":":\\"http://ww
#                         w.btcpower.com/assets/images/work/EV_Fast_Charger.png \\",",\\"order \\": 1,\\"resolution \\":":\\"990 *
#                         220 \\"}]}]}]},{"}]}]}]
#                 },{\\"lang \\":":\\"fr_US \\",",\\"imageScreen \\":[{":[{\\"screenId \\":":\\"SCREEN_SAVER imageSection \\":[{":[{\\"sectionName \\":":\\"FULL_SCREEN \\",",\\"imageData
# [{[{\\"duration \\": 30,\\"url \\":":\\"http://www.btcpower.com/assets/images/work/EV_Fast_Charger.png \\",",\\"order \\": 1,\\"resolution \\":":\\"1032 *
# 706 \\"}]},{"}]},{\\"sectionName \\":":\\"FULL_SCREEN \\",",\\"imageData \\":[{":[{\\"dura tion \\": 30,\\"url \\":":\\"http://www.btcpower.com/assets/images/work/EV_Fast_
# png \\",",\\"order \\": 2,\\"resolution \\":":\\"1032 *
# 706 \\"}]}]},{"}]}]},{\\"screenId \\":":\\"CHARGING_SCREEN \\",",\\"imageSection \\":[{":[{\\"sectionName \\":":\\"ADVERTISEMENT \\",",\\"imageData \\":[{":[{\\"duration \\": 30,\\"url \\":":\\"http
# ://www.btcpower.com/assets/images/work/EV_Fast_Charger.png \\",",\\"order \\": 1,\\"resolution \\":":\\"990 *
# 220 \\"}]}]},{"}]}]},{\\"screenId \\":":\\"PRICING_SCREEN \\",",\\"imageSection \\":[{":[{\\"sectionName \\":":\\"FULL_SCREEN \\",",\\"imageData \\":[{":[{\\"duration \\": 30,\\"url \\":":\\"http://ww
# w.btc power.com/assets/images/work/EV_Fast_Charger.png \\",",\\"order \\": 1,\\"resolution \\":":\\"990 * 220
#


                response = call_result.DataTransferPayload(
                    status=DataTransferStatus.accepted,
                    data=str({}),


                )
                print("server->cp , FetchImageInfo \n", response, "\n")
                return response



        #
        #


        # response = call_result.DataTransferPayload(
        #     status=DataTransferStatus.accepted,
        #     data="we get transfer data"
        # )
        # return response

#   send from server :
    # 1
    async def send_clear_cache_request(self):
        print("1.hello, clear cache request send to client")
        request = call.ClearCachePayload(

        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "ClearCache.req")

        response = await self.call(request)
        print(response.__dict__)
        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "ClearCache.con")


        if response.status == ClearCacheStatus.accepted:
            print("3.we can Clear cache")
        elif response.status == ClearCacheStatus.rejected:
            print("3.client rejected to clear cache")

    # 2
    async def send_remote_start_transaction(self):
        print("1.hello, remote start transaction request send to client")
        request = call.RemoteStartTransactionPayload(
            id_tag="transaction1",
            connector_id=1
        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "RemoteStartTransaction.req")
        print("serve -> cp , send_remote_start_transaction: \n", request, "\n")

        response = await self.call(request)

        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "RemoteStartTransaction.con")
        print("cp -> server, send_remote_start_transaction is:\n", response, "\n")

        if response.status == RemoteStartStopStatus.accepted:
            print("3.we can remote start transaction")
            # await self.set_charging_profile(limit=100)
        elif response.status == RemoteStartStopStatus.rejected:
            print("3.client rejected remote start transaction")

    # 3
    async def send_remote_stop_transaction(self):
        print("1.hello, remote stop transaction request send to client")
        request = call.RemoteStopTransactionPayload(
            transaction_id=111
        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "RemoteStopTransaction.req")
        print("server -> cp , send_remote_stop_transaction: \n", request, "\n")

        response = await self.call(request)

        print("cp -> server, send_remote_stop_transaction: \n", response, "\n")
        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "RemoteStopTransaction.con")
        if response.status == RemoteStartStopStatus.accepted:
            print("3.we can remote stop transaction")
        elif response.status == RemoteStartStopStatus.rejected:
            print("3.client rejected remote stop transaction")

    # 4
    async def set_charging_profile(self, limit):  #在 start transcation 或 remote start transcation中使用
        request = call.SetChargingProfilePayload(
            connector_id=0,            # The connector to which the charging profile applies. If connectorId = 0, the message contains an overall limit for the Charge Point.
            cs_charging_profiles={
                "chargingProfileId": 1,
                "transactionId":1,      #Optional
                "stackLevel":1,
                "chargingProfilePurpose": ChargingProfilePurposeType.chargepointmaxprofile,
                "chargingProfileKind": ChargingProfileKindType.absolute,
                "recurrencyKind": RecurrencyKind.daily,   # optional
                "validFrom":"2020-07-06T01:04:18.164785", # optional
                "validTo": "2020-10-06T01:04:18.164785",  # optional
                "chargingSchedule":{
                    "duration":600,                       # Optional. Duration of the charging schedule in seconds
                    "startSchedule": "2020-07-06T01:04:18.164785",   #Optional.
                    "chargingRateUnit": ChargingRateUnitType.watts,
                    "chargingSchedulePeriod":[{
                        "startPeriod": 10 ,
                        "limit": limit,    #  Charging rate limit during the schedule period, in the applicable chargingRateUnit, for example in Amperes or Watts. Accepts at most one digit fraction (e.g. 8.1).
                        "numberPhases":2
                    }],
                    "minChargingRate":2.1,
                }
            }
        )

        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "SetChargingProfile.req")
        print("server -> cp , set_charging_profile: \n", request, "\n")

        response = await self.call(request)

        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "SetChargingProfile.con")
        print("cp -> server, set_charging_profile: \n", response, "\n")


    # 5
    async def clear_charging_profile(self):
        request = call.ClearChargingProfilePayload(
            id=1,                        # Optional. The ID of the charging profile to clear.
            connector_id= 1,    # Optional. Specifies the ID of the connector for which to clear
                                # charging profiles. A connectorId of zero (0) specifies the charging
                                # profile for the overall Charge Point. Absence of this parameter
                                # means the clearing applies to all charging profiles that match the
                                # other criteria in the request.
            charging_profile_purpose = ChargingProfilePurposeType.txdefaultprofile,   #Optional. Specifies to purpose of the charging profiles that will be
                                                                                      #cleared, if they meet the other criteria in the request.
            stack_level=1,    #Optional. specifies the stackLevel for which charging profiles will be cleared, if they meet the other criteria in the request
        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "ClearChargingProfile.req")

        response = await self.call(request)
        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "ClearChargingProfile.con")
        print("clear_charging_profile response is ", response)

    # 6
    async def cancel_reservation(self):
        request = call.CancelReservationPayload(
            reservation_id=1,  #Required. Id of the reservation to cancel
        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "CancelReservation.req")

        response = await self.call(request)
        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "CancelReservation.con")
        print("cancel_reservation response is ", response)

    #7
    async def change_availability(self):
        request = call.ChangeAvailabilityPayload(
            connector_id=0 ,   #Required. The id of the connector for which availability needs to change. Id '0'
                               # (zero) is used if the availability of the Charge Point and all its connectors needs
                               # to change.
            type= AvailabilityType.inoperative   # Required. This contains the type of availability change that the Charge Point should perform.
        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "ChangeAvailability.req")

        response = await self.call(request)
        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "ChangeAvailability.con")
        print("change available response is", response)

    #8
    async def get_configuration(self):
        request = call.GetConfigurationPayload(
            key= ["max_current", "min_current", "max_power", "min_power"]      #Optional. List of keys for which the configuration value is requested.
        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "GetConfiguration.req")

        response = await self.call(request)
        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "GetConfiguration.con")
        print("get configuration response is", response)

    #9
    async def change_configuration(self):
        request = call.ChangeConfigurationPayload(
            key="max_current",  #Required. The name of the configuration setting to change. See for standard configuration key names and associated values
            value = "100",      #Required. The new value as string for the setting. See for standard configuration key names and associated values
        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "ChangeConfiguration.req")

        response = await self.call(request)
        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "ChangeConfiguration.con")
        print("change configuration response is", response)

    #10
    async def data_transfer(self):
        request =call.DataTransferPayload(
            vendor_id="MOEV",   #Required. This identifies the Vendor specific implementation
            message_id= "001",  #Optional. Additional identification field
            data = "hi???????", #Optional. Data without specified length or format.
        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "DataTransfer.req")

        response = await self.call(request)
        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "DataTransfer.con")
        print("data transfer response is ", response)

    #11
    async def get_local_list_version(self):
        request = call.GetLocalListVersionPayload(
        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "GetLocalListVersion.req")

        response = await self.call(request)
        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "GetLocalListVersion.con")
        print("get local list version response is ", response)

    #12
    async def send_local_list(self):
        request = call.SendLocalListPayload(
            list_version=2,     #Required. In case of a full update this is the version number of the full list.
                                # In case of a differential update it is the version number of the list after the update has been applied.
            local_authorization_list=[
                {"idTag":"001",
                 "idTagInfo":{
                     "expiryDate": "2020-12-12T00:00:00.792735",  #Optional. This contains the date at which idTag should be removed from the Authorization Cache.
                     "parentIdTag": "002",                        #Optional. This contains the parent-identifier.
                     "status":AuthorizationStatus.accepted,       #Required. This contains whether the idTag has been accepted or not by the Central System.
                    }
                 },
                {"idTag": "003",
                 "idTagInfo": {
                     "expiryDate": "2020-12-12T00:00:00.792735",
                     "parentIdTag": "004",
                     "status": AuthorizationStatus.accepted,
                    }
                 },
            ],
            update_type= UpdateType.full  #Required. This contains the type of update (full or differential) of this request.
        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "SendLocalList.req")

        response = await self.call(request)
        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "SendLocalList.con")
        print("send local list response is ",response)

    #13
    async def reset(self):
        request = call.ResetPayload(
            type= ResetType.hard   #Required. This contains the type of reset that the Charge Point should perform
        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "Reset.req")

        response = await self.call(request)
        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "Reset.con")
        print("reset response is ",response)

    #14
    async def unlock_connector(self):
        request =call.UnlockConnectorPayload(
            connector_id= 1,   #Required. This contains the identifier of the connector to be unlocked.
        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "UnlockConnector.req")

        response = await self.call(request)
        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "UnlockConnector.con")
        print("unlock connector is",response)

    #15
    async def update_firmware(self):
        request = call.UpdateFirmwarePayload(
            location="anyURI",    #Required. This contains a string containing a URI pointing to a location from which to retrieve the firmware.
            retries=3,            #Optional. This specifies how many times Charge Point must try to download the
                                  #firmware before giving up. If this field is not present, it is left to Charge Point to
                                  #decide how many times it wants to retry.
            retrieve_date=datetime.utcnow().isoformat(),    #Required. This contains the date and time after which the Charge Point is allowed to retrieve the (new) firmware.
            retry_interval=1800,  #Optional. The interval in seconds after which a retry may be attempted. If this
                                  #field is not present, it is left to Charge Point to decide how long to wait between attempts.
        )
        self.export_json_file(request.__dict__, "./dataFromServer2Cp", "UpdateFirmware.req")

        response = await self.call(request)
        self.export_json_file(response.__dict__, "./dataFromServer2Cp", "UpdateFirmware.con")
        print("update firmware is", response)


    async def authorized_payment(self,auth_data):
        print(auth_data)
        return True





async def on_connect(websocket, path):            # 等待client 链接   websocket 和 path 是client传来的参数，（变量名）
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.

    """

    charge_point_id = path.strip('/')              # 获得client 编号
    # charge_point_id = '12345'
    # print(charge_point_id)

    print("path from client is : %s" % path)
    # message_from_gui = await websocket.recv()

    # if charge_point_id.startswith("***",0,3):
    #     # print ("this message is from gui")
    #     print("charge point id is : %s" %charge_point_id)
    #     # message_from_gui = await websocket.recv()
    #     print("message from client is : %s" %message_from_gui)
    #
    #     return
    # else

    cp = ChargePoint(charge_point_id, websocket)   #创建ChargerPoint 实例化 记为 cp

    # 将每个cp添加到全局字典里
    EVSE_dict[charge_point_id] = cp

    await asyncio.gather(cp.start(),
                         # cp.send_clear_cache_request(),
                         # cp.send_remote_start_transaction(),
                         # cp.send_remote_stop_transaction(),
                         # cp.set_charging_profile()
                         # cp.clear_charging_profile()
                         # cp.cancel_reservation()
                         # cp.change_availability()
                         # cp.get_configuration()
                         # cp.change_configuration()
                         # cp.data_transfer()
                         # cp.get_local_list_version()
                         # cp.send_local_list()
                         # cp.reset()
                         # cp.unlock_connector()
                         # cp.update_firmware()
                         )

    # await cp.send_remote_stop_transation()
    # await cp.send_remote_start_transation()
    # await cp.send_clear_cache_request()

    # greeting = "this is server"
    # await websocket.send(greeting)
    # await cp.start()                            # cp启动  内置函数 start 在 ocpp.v16 import ChargePoint里

async def main():

    server = await websockets.serve(
        on_connect,
        '10.1.60.19',
        9000,
        subprotocols=['ocpp1.6']
    )

    await server.wait_closed()

if __name__ == '__main__':

    EVSE_dict = {}  # store all the EVSEs connected

    try:
        # asyncio.run() is used when running this example with Python 3.7 and
        # higher.
        asyncio.run(main())
    except AttributeError:
        # For Python 3.6 a bit more code is required to run the main() task on
        # an event loop.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
