from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
import logging
from collections import defaultdict
import json
import pandas as pd

# # Create your views here.
# def upload_csv(request):
#     file = request.FILES['file'] 
#     decoded_file = file.read().decode('utf-8').splitlines()
#     reader = csv.DictReader(decoded_file)
#     for row in reader:



def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "open_csv/upload_csv.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("open_csv:upload_csv"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("open_csv:upload_csv"))
        df = pd.read_csv(csv_file)
        messages.success(request, type(df))
        data = df.to_json(orient='split')
        """
        file_data = csv_file.read().decode("utf-8-sig")	
        	
        
        messages.success(request, type(df))
        lines = file_data.split("\n")
        # Here we used :-2 for removing /r
        header = lines.pop(0)[:-1].split(',')
		#loop over the lines and save them in db. If error , store as string and then display
        # messages.success(request, header)
        # it create header as key and intialize with a empty list
        data = defaultdict(list)
        data.fromkeys(header)

        for line in lines:						
            fields = line[:-1].split(",")
            if line:
                for i, head in enumerate(header):
                    data[head].append(fields[i])
        # converting data into json form
        data = json.dumps(data)
                    # 
                # data_list = []
                # data_list.append(fields[0])
                # data_list.append(fields[1])
                # data_list.append(fields[2])
                # data_list.append(fields[3][:-1])
                # data.append(fields)
			# try:
			# 	form = EventsForm(data_dict)
			# 	if form.is_valid():
			# 		form.save()					
			# 	else:
			# 		logging.getLogger("error_logger").error(form.errors.as_json())												
			# except Exception as e:
			# 	logging.getLogger("error_logger").error(repr(e))					
			# 	pass
        """
        return render(request, template_name="open_csv/show_csv.html", context={"csv_data": data})

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))

    
    return HttpResponseRedirect(reverse("open_csv:upload_csv"))
