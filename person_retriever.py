import requests
from bs4 import BeautifulSoup


def get_person(cedula):
    # start session
    mock_url = 'https://servicioselectorales.tse.go.cr/chc/consulta_cedula.aspx'
    with requests.session() as session:
        # get first mock request
        mock_request = session.get(mock_url)
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
        session.post(mock_url, data=form_data, headers=headers)

        # final response!
        final_response = session.get('https://servicioselectorales.tse.go.cr/chc/resultado_persona.aspx')
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

    return results
