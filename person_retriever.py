import requests
from bs4 import BeautifulSoup


def get_person(cedula):
    # start session
    mock_url = 'https://servicioselectorales.tse.go.cr/chc/'
    with requests.session() as session:
        # get first mock request
        mock_request = session.get(mock_url + 'consulta_cedula.aspx')
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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/94.0.4606.81 Safari/537.36 '
        }

        # send post request
        session.post(mock_url + 'consulta_cedula.aspx', data=form_data, headers=headers)

        # final response!
        final_response = session.get(mock_url + 'resultado_persona.aspx')
        with open("output1.html", "w") as file:
            file.write(str(final_response))
        final_soup = BeautifulSoup(final_response.text, 'html.parser')

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

        children_response = session.post(mock_url + 'resultado_persona.aspx', data=form_data2, headers=headers)
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
                children.append(child)
            results['children'] = children

    return results
