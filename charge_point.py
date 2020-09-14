import asyncio

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys
    sys.exit(1)

from ocpp.routing import on,after
from ocpp.v16 import call
from ocpp.v16 import call_result
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus, Action, ClearCacheStatus, RemoteStartStopStatus,\
    ChargingProfileStatus,Reason, ReadingContext,ValueFormat,Measurand,Phase,\
    Location,UnitOfMeasure,ChargePointErrorCode,ChargePointStatus,CancelReservationStatus,AvailabilityStatus\
    ,ConfigurationStatus,DataTransferStatus,UpdateStatus,ResetStatus,UnlockStatus

from datetime import datetime
import json

class ChargePoint(cp):  # cp 作为 ocpp 的 实例

    # client主动发送
    # 1
    async def boot_notification(self):           #
        request = call.BootNotificationPayload(
            charge_point_model="Optimus",        #Required. This contains a value that identifies the model of the ChargePoint.
            charge_point_vendor="NOEVmh_vendor", #Required. This contains a value that identifies the vendor of the ChargePoint.
            charge_box_serial_number= "1111",    #Optional. This contains a value that identifies the serial number of the Charge Box inside the Charge Point. Deprecated, will be removed in future version
            charge_point_serial_number="2222",   #Optional. This contains a value that identifies the serial number of the Charge Point.
            firmware_version= "3333", #Optional. This contains the firmware version of the Charge Point.
            iccid="4444",             #Optional. This contains the ICCID of the modem’s SIM card.
            imsi="5555",              #Optional. This contains the IMSI of the modem’s SIM card.
            meter_serial_number="6666",  # Optional. This contains the serial number of the main electrical meter of the Charge Point.
            meter_type="7777",           #Optional. This contains the type of the main electrical meter of the Charge Point.
        )

        response = await self.call(request)      

        if response.status ==  RegistrationStatus.accepted:
            print("Connected to central system!!!!!!!!.")

    # 2
    async def authorize(self):           #
        request = call.AuthorizePayload(
            id_tag="001gmh",              # Required. This contains the identifier that needs to be authorized.
        )

        response = await self.call(request)
        print("authorize response is ",response)

    # 3
    async def heart_beat(self):
        request = call.HeartbeatPayload(

        )
        response = await self.call(request)
        print("heart beat response is ",response)

    # 4
    async def start_transaction(self):           #
        request = call.StartTransactionPayload(
            connector_id=1,           #Required. This identifies which connector of the Charge Point is used.
            id_tag="001transaction",  #Required. This contains the identifier for which a transaction has to be started.
            meter_start= 0,           #Required. This contains the meter value in Wh for the connector at start of the transaction.
            reservation_id=0,         #Optional. This contains the id of the reservation that terminates as a result of this transaction.
            timestamp=datetime.utcnow().isoformat(),
        )
        response = await self.call(request)
        print("start_transaction response is", response)

    # 5
    async def stop_transaction(self):
        request = call.StopTransactionPayload(

            id_tag="001transaction",   # optional  Optional. This contains the identifier which requested to stop the charging. It is
                                       # optional because a Charge Point may terminate charging without the presence
                                       # of an idTag, e.g. in case of a reset. A Charge Point SHALL send the idTag if known.
            meter_stop=200,           # Required. This contains the meter value in Wh for the connector at end of the transaction.
            timestamp=datetime.utcnow().isoformat(),
            transaction_id = 11111,     # Required. This contains the transaction-id as received by the StartTransaction.conf.
            reason=Reason.local,       #Optional. This contains the reason why the transaction was stopped. MAY only be omitted when the Reason is "Local".
            #transaction_data={MeterValue}   # Optional. This contains transaction usage details relevant for billing purposes.
        )
        response = await self.call(request)
        print("stop_transaction response is",response)

    # 6
    async def meter_value(self):
        request = call.MeterValuesPayload(
            connector_id= 0,  # Required. This contains a number (>0) designating a connector of the Charge Point.‘0’ (zero) is used to designate the main powermeter.
            transaction_id= 111,  #Optional. The transaction to which these meter samples are related.
            meter_value=[{             #Required. The sampled meter values with timestamps.
                "timestamp":datetime.now().isoformat(),
                "sampledValue":[{
                    "value":"100",     #Required. Value as a “Raw” (decimal) number or “SignedData”. Field Type is
                                        #“string” to allow for digitally signed data readings. Decimal numeric values are
                                        #also acceptable to allow fractional values for measurands such as Temperature
                                        #and Current.
                    "context":ReadingContext.interruptionBegin,    #Optional. Type of detail value: start, end or sample. Default = “Sample.Periodic”
                    "format": ValueFormat.raw,                     #Optional. Raw or signed data. Default = “Raw”
                    "measurand":Measurand.currentExport,           #Optional. Type of measurement. Default = “Energy.Active.Import.Register”
                    "phase":Phase.l1,                               #  Optional. indicates how the measured value is to be interpreted. For instance
                                                                    # between L1 and neutral (L1-N) Please note that not all values of phase are
                                                                    # applicable to all Measurands. When phase is absent, the measured value is
                                                                    # interpreted as an overall value.
                    "location":Location.outlet,                    #Optional. Location of measurement. Default=”Outlet”
                    "unit":UnitOfMeasure.wh,                       #Optional. Unit of the value. Default = “Wh” if the (default) measurand is an “Energy” type.
                }]
            }]
        )
        response = await self.call(request)
        print("meter value response is ",response)

    # 7
    async def status_notification(self):
        request = call.StatusNotificationPayload(
            connector_id=0,   #  Required. The id of the connector for which the status is reported.
                                # Id '0' (zero) is used if the status is for the Charge Point main
                                # controller.
            error_code=ChargePointErrorCode.connectorLockFailure,  # Required. This contains the error code reported by the Charge Point.
            info="this is a big error" ,          #Optional. Additional free format information related to the error.
            status=ChargePointStatus.available,   #Required. This contains the current status of the Charge Point.
            timestamp=datetime.utcnow().isoformat(),  #Optional. The time for which the status is reported. If absent time of receipt of the message will be assumed
            vendor_id="MOEV",                         # Optional. This identifies the vendor-specific implementation
            vendor_error_code="MOEV 001 error",        #Optional. This contains the vendor-specific error code.
        )
        response = await self.call(request)
        print("status notification response is ", response)


    # special
    async def data_transfer(self):
        data ={
            "connectorId": 1,
            "paySessionId": "<Unique Integer ID per session>",
            "authData": [{
                "Payment Type": "CC_OCPP",
                "CCDATA": "UoJ5VffAL288roKIoPYDQGsmL+WKzgorg5BThTET97Ae29plmtKL2w",
                "decryptedDataLen": "40",
                "KSN": "kBAZC0XKkwAAJA",
                "vendorId": "magtek",
                "version": "< MAGTEK_API_VERSION >",
                "phone": "< DRIVER_PHONE_NUBER_ENTERED_FROM_CHARGER_SCREEN >",
                "email": "< DRIVER_EMAIL_ENTERED_FROM_CHARGER_SCREEN >",
                "priceCode": "< CURRENTLY_UNDEFINED >",
                }
            ],
            "timestamp": "<Current Timestamp>"
        }

        # data = {}

        data_j = json.dumps(data)

        request = call.DataTransferPayload(
            vendor_id="< EVSE_MANUFACTURER >",
            message_id="AuthorizedPayment.req",
            # message_id="FetchImageInfo.req",
            data=data_j,
        )


        response = await self.call(request)

        print("response is ", response)

        if response.status == RegistrationStatus.accepted:
            print("response.data is:", response.data)



    ### 接收请求 后的反应
    # 1
    @on(Action.ClearCache)
    def clear_cache_notification(self,**kwargs):
        print("clear cache receive is ",kwargs)
        print("2.client receive clear cache request and will return accepted")
        return call_result.ClearCachePayload(
            status=ClearCacheStatus.accepted
    )

    # 2
    @on(Action.RemoteStartTransaction)  #
    def remote_start_transaction_notification(self, **kwargs):
        print("remote_start_transaction receive is", kwargs)
        print("2.client receive remote start transaction request and will return accepted")
        return call_result.RemoteStartTransactionPayload(
            status=RemoteStartStopStatus.accepted
        )

    @after(Action.RemoteStartTransaction)
    async def after_remote_start_transaction_notification(self, **kwargs):
        await self.start_transaction()


    # 3
    @on(Action.RemoteStopTransaction)  #
    def remote_stop_transaction_notification(self, **kwargs):
        print("remote_stop_transaction receive is ", kwargs)
        print("2.client receive remote stop transaction request and will return accepted")
        return call_result.RemoteStopTransactionPayload(
            status=RemoteStartStopStatus.accepted
        )


    # 4
    @on(Action.SetChargingProfile)
    def set_charging_profile_notification(self,**kwargs):

        print("set charing profile receive is: \n", kwargs, "\n")
        return call_result.SetChargingProfilePayload(
            status=ChargingProfileStatus.accepted
        )

    # 5
    @on(Action.ClearChargingProfile)
    def clear_charging_profile_notification(self, **kwargs):
        print("clear charging profile receive is", kwargs)
        return call_result.ClearChargingProfilePayload(
            status=ClearCacheStatus.accepted
        )
    #6
    @on(Action.CancelReservation)
    def cancel_reservation_notification(self,**kwargs):
        print("cancel reservation receive is", kwargs)
        return call_result.CancelReservationPayload(
            status=CancelReservationStatus.accepted
        )

    #7
    @on(Action.ChangeAvailability)
    def change_availablility_notification(self,**kwargs):
        print("change availability receive is", kwargs)
        return call_result.ChangeAvailabilityPayload(
            status=AvailabilityStatus.accepted
        )

    #8
    @on(Action.GetConfiguration)
    def get_configuration_notification(self,**kwargs):
        print("get configuration receive is ",kwargs)
        return call_result.GetConfigurationPayload(
            configuration_key= [                              #Optional. List of requested or known keys
                {"key":"max_current","readonly":True,"value":"100"},
                {"key":"min_current","readonly":True,"value":"10"},
                {"key":"max_power", "readonly": False, "value": "200"},
                {"key":"min_power", "readonly": False, "value": "20"},
            ],
            unknown_key=["max_voltage","min_voltage"]
        )

    #9f
    @on(Action.ChangeConfiguration)
    def change_configuration_notification(self,**kwargs):
        print("change configuration receive is", kwargs)
        return call_result.ChangeConfigurationPayload(
            status=ConfigurationStatus.accepted,    # Required. Returns whether configuration change has been accepted.
        )



    #10
    @on(Action.DataTransfer)
    def data_transfer_notification(self,**kwargs):
        print("data transfer receive is ",kwargs)
        return call_result.DataTransferPayload(
            status=DataTransferStatus.accepted,    #Required. This indicates the success or failure of the data transfer.
            data="I receive the data",             #Optional. Data in response to request.
        )



    #11
    @on(Action.GetLocalListVersion)
    def get_local_list_version_notification(self,**kwargs):
        print("get local list version receive is" , kwargs)
        return call_result.GetLocalListVersionPayload(
            list_version=1    # Required. This contains the current version number of the local authorization list in the Charge Point.
        )


    #12
    @on(Action.SendLocalList)
    def send_local_list_notification(self,**kwargs):
        print("send local list receive is", kwargs)
        return call_result.SendLocalListPayload(
            status=UpdateStatus.accepted    #Required. This indicates whether the Charge Point has successfully received and applied the update of the local authorization list.
        )

    #13
    @on(Action.Reset)
    def reset_notification(self,**kwargs):
        print("reset receive is",kwargs)
        return call_result.ResetPayload(
            status=  ResetStatus.accepted         #Required. This indicates whether the Charge Point is able to perform the reset.
        )

    #14
    @on(Action.UnlockConnector)
    def unlock_connector_notification(self,**kwargs):
        print("unlock connector receive is",kwargs)
        return call_result.UnlockConnectorPayload(
            status= UnlockStatus.unlocked         #Required. This indicates whether the Charge Point has unlocked the connector.
        )

    #15
    @on(Action.UpdateFirmware)
    def unlock_connector_notification(self,**kwargs):
        print("update firmware is",kwargs)
        return call_result.UpdateFirmwarePayload(
        )
        



async def main():
    async with websockets.connect(                   #
        'ws://10.1.60.19:9000/CP_1',                #
         subprotocols=['ocpp1.6']
    ) as ws:

        cp = ChargePoint('CP_1', ws)          #

        await asyncio.gather(
                             cp.start(),
                             # cp.boot_notification(),
                             # cp.authorize(),
                             # cp.heart_beat(),
                             # cp.start_transaction(),
                             # cp.stop_transaction(),
                             # cp.meter_value(),
                             # cp.status_notification(),
                             cp.data_transfer(),
                             )


if __name__ == '__main__':
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