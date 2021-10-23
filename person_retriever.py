import requests
import traceback
from bs4 import BeautifulSoup

url = 'https://servicioselectorales.tse.go.cr/chc/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/94.0.4606.81 Safari/537.36 '
}


def return_person(session):
    response = session.get(url + 'resultado_persona.aspx')
    final_soup = BeautifulSoup(response.text, 'html.parser')

    results = {
        'cedula': final_soup.find('span', {"id": "lblcedula"}).find('font').get_text(),
        'nombreCompleto': final_soup.find('span', {"id": "lblnombrecompleto"}).find('font').get_text(),
        'conocidoComo': final_soup.find('span', {"id": "lblconocidocomo"}).find('font').get_text(),
        'nombrePadre': final_soup.find('span', {"id": "lblnombrepadre"}).find('font').get_text(),
        'cedulaPadre': final_soup.find('span', {"id": "lblid_padre"}).find('font').get_text(),
        'nombreMadre': final_soup.find('span', {"id": "lblnombremadre"}).find('font').get_text(),
        'cedulaMadre': final_soup.find('span', {"id": "lblid_madre"}).find('font').get_text(),
        'difunto': final_soup.find('span', {"id": "lbldefuncion2"}).find('font').get_text(),
        'fechaNacimiento': final_soup.find('span', {"id": "lblfechaNacimiento"}).find('font').get_text(),
        'nacionalidad': final_soup.find('span', {"id": "lblnacionalidad"}).find('font').get_text()
    }

    # gather all the important data
    view_state2 = final_soup.select("#__VIEWSTATE")[0]['value']
    view_state_gen2 = final_soup.select("#__VIEWSTATEGENERATOR")[0]['value']
    event_validation2 = final_soup.select("#__EVENTVALIDATION")[0]['value']
    form_data2 = (
        ('ScriptManager1', 'ctl06|btnMostrarNacimiento'),
        ('__VIEWSTATE', view_state2),
        ('__VIEWSTATEGENERATOR', view_state_gen2),
        ('__EVENTVALIDATION', event_validation2),
        ('hdnCodigoAccionMarginal', '1'),
        ('hdnFechaSucesoMatrimonio', ''),
        ('__EVENTTARGET', 'btnConsultaCedula'),
        ('__ASYNCPOST', 'true'),
        ('btnMostrarNacimiento', 'Mostrar')
    )

    children_response = session.post(url + 'resultado_persona.aspx', data=form_data2, headers=headers)
    children_soup = BeautifulSoup(children_response.text, 'html.parser')
    children_table = children_soup.find('table', {"id": "Gridhijos"})

    # if there are no children, return
    if children_table:
        with open("output3.html", "w") as file:
            file.write(str(children_table))

        # if there are
        children = []
        for tr in children_table.find_all('tr'):
            i = 0
            child = {}
            for td in tr.find_all('td'):
                if not td.has_attr('some_attribute'):
                    if i == 0:
                        i = i + 1
                        continue
                    elif i == 1:
                        child['cedula'] = td.get_text()
                    elif i == 2:
                        child['fecha_nacimiento'] = td.get_text()
                    elif i == 3:
                        child['nombre'] = td.get_text()
                    i = i + 1
            if child != {}:
                children.append(child)
        results['children'] = children

    return results


def get_person(cedula):
    # start session
    with requests.session() as session:
        # get first mock request
        mock_request = session.get(url + 'consulta_cedula.aspx')
        mock_soup = BeautifulSoup(mock_request.text, 'html.parser')
        mock_request.close()

        # gather all the important data
        view_state = mock_soup.select("#__VIEWSTATE")[0]['value']
        view_state_gen = mock_soup.select("#__VIEWSTATEGENERATOR")[0]['value']
        event_validation = mock_soup.select("#__EVENTVALIDATION")[0]['value']
        form_data = (
            ('ScriptManager1', 'UpdatePanel1|btnConsultaCedula'),
            ('__VIEWSTATE', view_state),
            ('__VIEWSTATEGENERATOR', view_state_gen),
            ('__EVENTVALIDATION', event_validation),
            ('txtcedula', cedula),
            ('__EVENTTARGET', 'btnConsultaCedula'),
            ('__ASYNCPOST', 'true'),
            ('btnConsultaCedula', 'Consultar')
        )

        # send post request
        session.post(url + 'consulta_cedula.aspx', data=form_data, headers=headers)

    return return_person(session)


def get_person_by_name(nombre='', apellido1='', apellido2=''):
    with requests.session() as session:
        mock_request = session.get(url + 'consulta_nombres.aspx')
        mock_soup = BeautifulSoup(mock_request.text, 'html.parser')
        mock_request.close()

        # gather all the important data
        view_state = mock_soup.select("#__VIEWSTATE")[0]['value']
        view_state_gen = mock_soup.select("#__VIEWSTATEGENERATOR")[0]['value']
        event_validation = mock_soup.select("#__EVENTVALIDATION")[0]['value']
        form_data = (
            ('ScriptManager1', 'UpdatePanel1|btnConsultarNombre'),
            ('__VIEWSTATE', view_state),
            ('__VIEWSTATEGENERATOR', view_state_gen),
            ('__EVENTVALIDATION', event_validation),
            ('txtnombre', nombre),
            ('txtapellido1', apellido1),
            ('txtapellido2', apellido2),
            ('__EVENTTARGET', 'btnConsultaCedula'),
            ('__ASYNCPOST', 'true'),
            ('btnConsultarNombre', 'Consultar')
        )

        # send post request
        session.post(url + 'consulta_nombres.aspx', data=form_data, headers=headers)

        # matches
        matches_response = session.get(url + 'muestra_nombres.aspx')
        matches_soup = BeautifulSoup(matches_response.text, 'html.parser')

        # Get match count
        try:
            matches_list = matches_soup.find('span', {"id": "chk1"}).find_all('input')
        except:
            return False
        print(len(matches_list))

        # Get important data
        view_state2 = matches_soup.select("#__VIEWSTATE")[0]['value']
        view_state_gen2 = matches_soup.select("#__VIEWSTATEGENERATOR")[0]['value']
        event_validation2 = matches_soup.select("#__EVENTVALIDATION")[0]['value']
        form_data2 = (
            ('__LASTFOCUS', ''),
            ('__EVENTTARGET', ''),
            ('__EVENTARGUMENT', ''),
            ('__VIEWSTATE', view_state2),
            ('__VIEWSTATEGENERATOR', view_state_gen2),
            ('__EVENTVALIDATION', event_validation2),
            ('Button1', 'Realizar consulta'),
        )

        # Add each match to the form
        for i in range(len(matches_list)):
            form_data2 = form_data2 + ((str(('chk1$'+str(i))), 'on'),)

        # Do the POST
        session.post(url + 'muestra_nombres.aspx', data=form_data2, headers=headers)

        # GET the page of each match
        match_response = session.get(url + 'resultado_persona.aspx')
        match_soup = BeautifulSoup(match_response.text, 'html.parser')

        with open("output4.html", "w", encoding='utf8') as file:
            file.write(str(match_soup))

        results = [{
            'cedula': match_soup.find('span', {"id": "lblcedula"}).find('font').get_text(),
            'nombreCompleto': match_soup.find('span', {"id": "lblnombrecompleto"}).find('font').get_text(),
            'conocidoComo': match_soup.find('span', {"id": "lblconocidocomo"}).find('font').get_text(),
            'nombrePadre': match_soup.find('span', {"id": "lblnombrepadre"}).find('font').get_text(),
            'cedulaPadre': match_soup.find('span', {"id": "lblid_padre"}).find('font').get_text(),
            'nombreMadre': match_soup.find('span', {"id": "lblnombremadre"}).find('font').get_text(),
            'cedulaMadre': match_soup.find('span', {"id": "lblid_madre"}).find('font').get_text(),
            'difunto': match_soup.find('span', {"id": "lbldefuncion2"}).find('font').get_text(),
            'fechaNacimiento': match_soup.find('span', {"id": "lblfechaNacimiento"}).find('font').get_text(),
            'nacionalidad': match_soup.find('span', {"id": "lblnacionalidad"}).find('font').get_text(),
            'children': 'UNKNOWN'
        }]

        view_state3 = match_soup.select("#__VIEWSTATE")[0]['value']
        view_state_gen3 = match_soup.select("#__VIEWSTATEGENERATOR")[0]['value']
        event_validation3 = match_soup.select("#__EVENTVALIDATION")[0]['value']
        form_data3 = (
            ('ScriptManager1', 'UpdatePanel4|cmbsiguient'),
            ('hdnCodigoAccionMarginal', '1'),
            ('hdnFechaSucesoMatrimonio', ''),
            ('__LASTFOCUS', ''),
            ('__EVENTTARGET', 'cmbsiguiente'),
            ('__EVENTARGUMENT', ''),
            ('__VIEWSTATE', view_state3),
            ('__VIEWSTATEGENERATOR', view_state_gen3),
            ('__EVENTVALIDATION', event_validation3),
            ('__ASYNCPOST', 'true')
        )

        next_response = session.post(url + 'resultado_persona.aspx', data=form_data3, headers=headers)
        last_query = {}
        query_count = 0
        for i in range(len(matches_list)-2):
            try:
                match_soup = BeautifulSoup(next_response.text, 'html.parser')

                all_text = match_soup.findAll(text=True)
                important_text = all_text[len(all_text)-1]
                important_text = important_text.split('|')
                for ii in range(len(important_text)):
                    if important_text[ii].isdigit() or important_text[ii] == 'hiddenField':
                        continue
                    if important_text[ii] == '__LASTFOCUS':
                        last_focus4 = important_text[ii+1]
                    if important_text[ii] == '__EVENTTARGET':
                        event_target4 = important_text[ii+1]
                    if important_text[ii] == '__EVENTARGUMENT':
                        event_argument4 = important_text[ii+1]
                    if important_text[ii] == '__VIEWSTATE':
                        view_state4 = important_text[ii+1]
                    if important_text[ii] == '__VIEWSTATEGENERATOR':
                        view_state_gen4 = important_text[ii+1]
                    if important_text[ii] == '__EVENTVALIDATION':
                        event_validation4 = important_text[ii+1]

                form_data4 = (
                    ('ScriptManager1', 'UpdatePanel4|cmbsiguient'),
                    ('hdnCodigoAccionMarginal', '1'),
                    ('hdnFechaSucesoMatrimonio', ''),
                    ('__LASTFOCUS', last_focus4),
                    ('__EVENTTARGET', 'cmbsiguiente'),
                    ('__EVENTARGUMENT', event_argument4),
                    ('__VIEWSTATE', view_state4),
                    ('__VIEWSTATEGENERATOR', view_state_gen4),
                    ('__EVENTVALIDATION', event_validation4),
                    ('__ASYNCPOST', 'true')
                )

                next_response = session.post(url + 'resultado_persona.aspx', data=form_data4, headers=headers)
                match_soup = BeautifulSoup(next_response.text, 'html.parser')

                last_query = {
                    'cedula': match_soup.find('span', {"id": "lblcedula"}).get_text(),
                    'nombreCompleto': match_soup.find('span', {"id": "lblnombrecompleto"}).get_text(),
                    'conocidoComo': match_soup.find('span', {"id": "lblconocidocomo"}).get_text(),
                    'nombrePadre': match_soup.find('span', {"id": "lblnombrepadre"}).get_text(),
                    'cedulaPadre': match_soup.find('span', {"id": "lblid_padre"}).get_text(),
                    'nombreMadre': match_soup.find('span', {"id": "lblnombremadre"}).get_text(),
                    'cedulaMadre': match_soup.find('span', {"id": "lblid_madre"}).get_text(),
                    'difunto': match_soup.find('span', {"id": "lbldefuncion2"}).get_text(),
                    'fechaNacimiento': match_soup.find('span', {"id": "lblfechaNacimiento"}).get_text(),
                    'nacionalidad': match_soup.find('span', {"id": "lblnacionalidad"}).get_text(),
                    'children': 'UNKNOWN'
                }

                results.append(last_query)

                # print('query #'+str(query_count+1)+' OK')
            except:
                with open("output5.html", "w", encoding='utf8') as file:
                    file.write(str(match_soup))
                # print('query #'+str(query_count+1)+' ERROR')
                # print(traceback.format_exc())

            query_count += 1

        # print(last_query)
    return results
