def substation_list(request):
    if request.user.is_authenticated:
        operational_subs = request.user.operational_staff.all()
        administrative_subs = request.user.administrative_staff.all()
        admin_opj_subs = request.user.admin_opj.all()

        all_subs = (list(operational_subs) +
                    list(administrative_subs) +
                    list(admin_opj_subs))
        unique_subs = list(set(all_subs))
    else:
        unique_subs = []

    return {'unique_subs': unique_subs}
