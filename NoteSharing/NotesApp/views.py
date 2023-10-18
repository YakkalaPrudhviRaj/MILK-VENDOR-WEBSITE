from django.shortcuts import render,redirect, get_object_or_404
from .forms import UsForm,Adrolech,TchPf,DchPf,UsupForm,StForm,DtForm,NoteForm
from django.contrib import messages
from .models import User,TProfile,SProfile,DProfile,Orders, Notes
import secrets
# Create your views here.

def home(request):
	return render(request,'notehtmls/home.html')

def about(request):
	return render(request,'notehtmls/about.html')

def contact(request):
	return render(request,'notehtmls/contact.html')

def register(request):
	if request.method == "POST":
		u = UsForm(request.POST)
		if u.is_valid():
			d=u.save(commit=False)
			messages.success(request,f"{d.username} User Created Successfully")
			d.save()
			return redirect('/login')
	else:
		u = UsForm()
	return render(request,'notehtmls/register.html',{'us':u})

def rolechange(request):
	k = User.objects.all()
	return render(request,'notehtmls/role.html',{'u':k})

def roleupdate(request,t):
	g = User.objects.get(id=t)
	if request.method == "POST":
		n = Adrolech(request.POST,instance=g)
		if n.is_valid():
			n.save()
			messages.success(request,"Role Updated Successfully")
			return redirect('/roles')
	n = Adrolech(instance=g)
	return render(request,'notehtmls/roleupdate.html',{'v':n})

def profile(request):
	return render(request,'notehtmls/profile.html')

def updateprofile(request):
	h = User.objects.get(id=request.user.id)
	d = []
	if h.role == 'T':
		c = TProfile.objects.filter(tch_id=request.user.id)
		for i in c:
			d.append(i.tch_id)
		if request.user.id not in d:
			if request.method == "POST":
				v = UsupForm(request.POST,request.FILES,instance=h)
				s = TchPf(request.POST)
				if v.is_valid() and s.is_valid():
					n = v.save(commit=False)
					n.is_teacher = 1
					n.save()
					r = s.save(commit=False)
					r.tch_id = request.user.id
					r.save()
					return redirect('/pfle')
			v = UsupForm(instance=h)
			s = TchPf()
			return render(request,'notehtmls/upprofile.html',{'y':v,'n':s})
		else:
			f = TProfile.objects.get(tch_id=request.user.id)
			if request.method == "POST":
				v = UsupForm(request.POST,request.FILES,instance=h)
				s = TchPf(request.POST,instance=f)
				if v.is_valid() and s.is_valid():
					v.save()
					s.save()
					return redirect('/pfle')
			v = UsupForm(instance=h)
			s = TchPf(instance=f)
			return render(request,'notehtmls/upprofile.html',{'y':v,'n':s})
	elif h.role == 'D':
		x = DProfile.objects.filter(dch_id=request.user.id)
		u = []
		for i in x:
			u.append(i.dch_id)
		if request.user.id not in u:
			if request.method == "POST":
				v = UsupForm(request.POST,request.FILES,instance=h)
				g = DtForm(request.POST)
				if v.is_valid() and g.is_valid():
					a = v.save(commit=False)
					a.is_doctor = 1
					a.save()
					e = g.save(commit=False)
					e.dch_id=request.user.id
					e.save()
					return redirect('/pfle')
			v = UsupForm(instance=h)
			g = DtForm()
			return render(request,'notehtmls/upprofile.html',{'y':v,'m':g})	
		else:
			f = TProfile.objects.get(dch_id=request.user.id)
			if request.method == "POST":
				v = UsupForm(request.POST,request.FILES,instance=h)
				s = DchPf(request.POST,instance=f)
				if v.is_valid() and s.is_valid():
					v.save()
					s.save()
					return redirect('/pfle')
			v = UsupForm(instance=h)
			s = DchPf(instance=f)
			return render(request,'notehtmls/upprofile.html',{'y':v,'n':s})
	elif h.role == 'S':
		x = SProfile.objects.filter(stdnt_id=request.user.id)
		u = []
		for i in x:
			u.append(i.stdnt_id)
		if request.user.id not in u:
			if request.method == "POST":
				v = UsupForm(request.POST,request.FILES,instance=h)
				g = StForm(request.POST)
				if v.is_valid() and g.is_valid():
					a = v.save(commit=False)
					a.is_student = 1
					a.save()
					e = g.save(commit=False)
					e.stdnt_id=request.user.id
					e.save()
					return redirect('/pfle')
			v = UsupForm(instance=h)
			g = StForm()
			return render(request,'notehtmls/upprofile.html',{'y':v,'d':g})
		
		else:
			q = SProfile.objects.get(stdnt_id=request.user.id)
			if request.method == "POST":
				v = UsupForm(request.POST,request.FILES,instance=h)
				g = StForm(request.POST,instance=q)
				if v.is_valid() and g.is_valid():
					v.save()
					g.save()
					return redirect('/pfle')
			v = UsupForm(instance=h)
			g = StForm(instance=q)
			return render(request,'notehtmls/upprofile.html',{'y':v,'d':g})
	else:
		pass

def noteslist(request):
	n = Notes.objects.filter(usr_id=request.user.id)
	if request.method == "POST":
		c = NoteForm(request.POST,request.FILES)
		if c.is_valid():
			z = c.save(commit=False)
			z.sckey = secrets.token_hex(2)
			z.usr_id = request.user.id
			z.save()
			return redirect('/notes')
	c = NoteForm()
	return render(request,'notehtmls/notelist.html',{'p':c,'z':n})


def notesliststudent(request):
	objects= []
	h = SProfile.objects.filter(stdnt_id=request.user.id)
	branch_values = [profile.branch for profile in h]
	if request.method == "GET":
		objects_list= Notes.objects.filter()
		for note in objects_list:
			if note.branch == branch_values[0]:
				objects.append(note)
		c = NoteForm(request.GET, request.FILES)
		if c.is_valid():
			z = c.save(commit=False)
			z.sckey = secrets.token_hex(2)
			z.save()
			return redirect('/notesStudent')
	# Create an instance of the form
	c = NoteForm()
	return render(request, 'notehtmls/noteliststudent.html', {'p': c,'z': objects})

# def payment(request,id):
# 	objects_list = Notes.objects.filter(id=id)
# 	c = NoteForm(request.GET, request.FILES)
# 	if c.is_valid():
# 		z = c.save(commit=False)
# 		z.sckey = secrets.token_hex(2)
# 		z.save()
# 		return redirect('/payment')
# 	c = NoteForm()
# 	return render(request, 'notehtmls/payment.html', {'p': c,'z': objects_list})	

def payment(request, id):
	objects_list = Notes.objects.filter(id=id)
	c = NoteForm(request.POST, request.FILES)

	if request.method == 'POST':
		# Handle form submission
		selected_payment_method = request.POST.get('paymentMethod')
		if selected_payment_method == 'upi':
			# Check if a file is uploaded for UPI payment
			transaction_screenshot = request.FILES.get('transactionScreenshot')
			if not transaction_screenshot:
				# File is mandatory for UPI payment
				return render(request, 'notehtmls/payment.html', {'p': c, 'z': objects_list, 'error_message': 'Please upload a transaction screenshot for UPI payment.'})
		# Extract cart, address, and payment method from the form data
		cart = request.POST.get("cart_data")  # You need to adapt this based on your form
		address = request.POST.get("submittedAddress")
		payment_method = request.POST.get("paymentMethod")
		print(address,payment_method)

		# Create and save a new order
		order = Order(user=request.user, cart=cart, address=address, payment_method=payment_method)
		order.save()
		# Redirect to the success page after successful payment
		return redirect('/success')
	return render(request, 'notehtmls/payment.html', {'p': c, 'z': objects_list})


def edit_note(request, id):
    note = get_object_or_404(Notes, id=id)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('ntlist')  # Redirect to the notes list page
    else:
        form = NoteForm(instance=note)

    return render(request, 'notehtmls/edit_note.html', {'form': form, 'note': note})

def delete_note(request, id):
    note = get_object_or_404(Notes, id=id)

    if request.method == 'POST':
        note.delete()
        return redirect('ntlist')  # Redirect to the notes list page

    return render(request, 'notehtmls/delete_note.html', {'note': note})
def merchantList(request):
	c = User.objects.filter(is_teacher =1)
	details={}
	for i in c:
		print(i.id)
		t = TProfile.objects.filter(tch_id = i.id)
		print(t)
		details[i.id]= { "location": t[0].branch, "username":i.username, "contact": i.mb}
	return render(request, 'notehtmls/merchantlist.html', {'z': details })

def order_list(request):
	o = Orders.objects.all()

	print(o[0].address)
	return render(request, 'notehtmls/orders.html', {'orders': o })

def doctorlist(request):
	c = User.objects.filter(is_doctor =1)
	details={}
	for i in c:
		print(i.id)
		t = DProfile.objects.filter(dch_id = i.id)
		print(t)
		if t:
			details[i.id]= { "location": t[0].branch, "username":i.username, "contact": i.mb}
	return render(request, 'notehtmls/doctors.html', {'z': details })