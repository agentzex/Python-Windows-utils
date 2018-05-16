from collections import OrderedDict
import psutil


AV_TO_PROCESS_NAME = OrderedDict()
#AntiViruses processes names:

AV_TO_PROCESS_NAME["AdAwareService.exe"] = "AdAware"
AV_TO_PROCESS_NAME["AvastSvc.exe"] = "Avast"
AV_TO_PROCESS_NAME["AVGSvc.exe"] = "AVG"
AV_TO_PROCESS_NAME["Avira.ServiceHost.exe"] = "Avira"
AV_TO_PROCESS_NAME["vsserv.exe"] = "BitDefender"
AV_TO_PROCESS_NAME["cmdagent.exe"] = "Comodo"
AV_TO_PROCESS_NAME["EMET_Service.exe"] = "Windows Enhanced Mitigation Experience Toolkit"
AV_TO_PROCESS_NAME["ekrn.exe"] = "ESET"
AV_TO_PROCESS_NAME["GDFirewallTray.exe"] = "GData"
AV_TO_PROCESS_NAME["fshoster32.exe"] = "F-secure"
AV_TO_PROCESS_NAME["hmpalert.exe"] = "Hitmanpro"
AV_TO_PROCESS_NAME["avp.exe"] = "Kaspersky"
AV_TO_PROCESS_NAME["MBAMService.exe"] = "Malwarebytes"
AV_TO_PROCESS_NAME["mcapexe.exe"] = "Mcafee"
AV_TO_PROCESS_NAME["nsbu.exe"] = "Norton"
AV_TO_PROCESS_NAME["PSUAService.exe"] = "Panda"
AV_TO_PROCESS_NAME["MsMpEng.exe"] = "Windows Defender"


def check_process_to_av(process_name):
    for av_process_name in AV_TO_PROCESS_NAME.keys():
        if process_name.lower() == av_process_name.lower():
            return AV_TO_PROCESS_NAME[av_process_name]
    return None


def detect_av():
    found_avs = []
    c = psutil.process_iter()
    for process in c:
        av_found = check_process_to_av(str(process.name()))
        if av_found is not None:
            found_avs.append(av_found)
    return found_avs





if __name__ == "__main__":
    # Returns a list of found AntiViruses products on this machine
    print detect_av()