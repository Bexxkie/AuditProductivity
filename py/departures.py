import interactor
import shared



    #
    # I need to find a better way to do this
    # I don't want to need to use the 'heartbeat ' style like
    # on the pure py version
    #
    # I need to add some kind of interrupt system
    # like ctl+c in console

def departure():
    # reports_state_list + 'departures'
    # so this one is simple, it just needs to--
    # --open the reporting window, >> 'departures' >> input date (tomorrow)--
    # -->> tab(x2) to update other time elements >> click 'btn_print'
    #
    # can wait for returns 1
    interactor.load_reports('departures')
    curDate = shared.update_time()
    interactor.type_object(curDate.strftime("%m-%d-%y"))
    interactor.type_object("tab", True, 2)
    interactor.click_object(interactor.find_object("btn_print"))
