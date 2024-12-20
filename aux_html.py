from xhtml2pdf import pisa

def html_inicio():
	'''
	Funcion para el inicio del documento
	@param str style_path
	@param str titulo_h1
	@param str fecha_informe: fecha de generacion del informe
	@param str inicio_informe: fecha de inicio de datos
	@param str fin_informe: fecha de inicio de datos
	@param str machine_name: nombre de la máquina
	@param str charset
		pc: ISO-8859-1
		servidor: charset=UTF-8
	@return str
	'''
	solucion = ("<html>"
				+"<head>"
				+"<style>"
				+"body {font-family: Helvetica, Arial, sans-serif; color: #444444;font-size: 11pt;margin-left: 15px;margin-right: 15px;}"
				+'.titulo {font-size: 25pt;margin-top: 5px;margin-bottom: 5px;margin-left: 10px;margin-right: 10px;color: #417BCC;}'
				+'.subtitulo {font-size: 15pt;margin-top:10px;margin-bottom: 0px;margin-left: 10px;margin-right: 10px;}'
				+'.imagen {margin-top: 10px;margin-bottom: 10px;margin-left: 10px;margin-right: 10px;}'
				+'.sp{ page-break-after: always;}'
				+"table {table-layout: auto; width: 100%;background-color: #fefefe;border: 1px solid #444444;border-collapse: collapse;padding: 1px;}"
				+"th { width: auto; background-color: #dddddd}"
				+"td { width: auto}"
				+"</style>"
				+"</head>"
				+"<body>")
	return solucion

def convert_html_to_pdf(html_string, pdf_path):
    with open(pdf_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)
        
    return not pisa_status.err

def tabla_str(df):
    df = df.round(3).astype('str')
    for col in df:
        df.loc[df[col] == 'nan',col] = ''
    return df


def escribir_html(sol, img_file):
    df_medios_H929 = sol['df_medios_H929']
    df_dif_H929 = sol['df_dif_H929']
    df_dif_perc_H929 = sol['df_dif_perc_H929']
    df_medios_KMS28 = sol['df_medios_KMS28']
    df_dif_KMS28 = sol['df_dif_KMS28']
    df_dif_perc_KMS28 = sol['df_dif_perc_KMS28']
    html = html_inicio()

    html+= '<div class = "titulo"><b> H929</b></div>'
    html += '<div class = "imagen"><img src="'+img_file+ '\\Valores_H929.png"></img></div>'
    html += '<div class = "imagen"><img src="'+img_file+ '\\proliferacion_H929.png"></img></div>'

    html+= '<div class = "subtitulo">Valores medios</div>'
    df_print = df_medios_H929.copy()
    html +=  df_print.round(3).transpose().to_html()

    html+= '<div class = "subtitulo">Diferencias medias</div>'
    df_print = df_dif_H929.copy()
    html +=  df_print.round(3).transpose().to_html()

    html+= '<div class = "subtitulo">Proliferación</div>'
    df_print = df_dif_perc_H929.copy()
    html += df_print.round().transpose().to_html()

    html+= '<div class = "titulo"><b> KMS28</b></div>'
    html += '<div class = "imagen"><img src="'+img_file+ '\\Valores_KMS28.png"></img></div>'
    html += '<div class = "imagen"><img src="'+img_file+ '\\proliferacion_KMS28.png"></img></div>'

    html+= '<div class = "subtitulo">Valores medios</div>'
    df_print = df_medios_KMS28.copy()
    html +=  df_print.round(3).transpose().to_html()

    html+= '<div class = "subtitulo">Diferencias medias</div>'
    df_print = df_dif_KMS28.copy()
    html +=  df_print.round(3).transpose().to_html()

    html+= '<div class = "subtitulo">Proliferación</div>'
    df_print = df_dif_perc_KMS28.copy()
    html += df_print.round().transpose().to_html()

    html +='</body>'
    html += '</html>'
    with open("file.html", "w") as file:
        file.write(html)
    # Generate PDF
    pdf_path = "example.pdf"
    if convert_html_to_pdf(html, pdf_path):
        print(f"PDF generated and saved at {pdf_path}")
    else:
        print("PDF generation failed")