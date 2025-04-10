import os

# Ordered list of student names
students = [
    "ABEL PRAISE GOD", "AKIOMA BRIGHT", "AKPAN ESTHER KINGSLEY", "ALAUSA GIFT INIOLUWA", 
    "AMOS ESTHER ALUWAYE", "ANTHONY REJOICE", "AUGUSTINE GOLD", "BARINE TOM GIFT", 
    "BARITURE BARISIDO MIRIAM", "CHIGOZIE CHIZARAM", "CHIJIOKE DESIRE CHIOMA", "CHIKA BENITA", 
    "CHIMA CHINASA CHRISTABEL", "CHRISTOPHER JULET OKON", "CYRIL ARCHIBONG DESTINY", 
    "EDEM CHRISTIANA MICHAEL", "TIMOTHY ABIGAIL", "EMMANUEL CHUKWUCHIDERA", "EMMANUEL ESTHER UKO", 
    "EMMANUEL UYIME DESIRE", "ENIWOAKE PRECIOUS", "ETIM DEBORAH LARRY", "ETUK PEACE SAMUEL", 
    "EXOSE AFFADEYI", "UGBUNU FAVOUR OGHENENYERO", "FARUK SAADATU", "FRIDAY BARIMUE ESTHER", 
    "FRIDAY GOODNEWS", "IMOH AWESOME BASSEY", "IKECHUKWU REJOICE AMARACHI", "ITORO GLORY JAMES", 
    "JACOB DESTINY", "JOSEPH SUNDAY FAITH", "JOSHUA MIRACLE IKOYO", "JUMBO BLESSING", 
    "LEGBARA TAANABEBABARI", "MONDAY GOODNEWS", "MONDAY ROSEMARY", "NKEMAKOLAM MIRACLE", 
    "NWAFOR VICTORY AMARACHI", "NWAWULU CHIKAMSO MARY ANN", "NWIGBARATO SALVATION S.K", 
    "NZEDIEGWU CHRISTABEL", "OBOMANU MARVELLOUS G", "GODSWILL BRIGHTNESS", "OHANAGOROM ROSEMARY", 
    "OKAFOR DIVINE", "OLORUNDA AWOTUNDE HONOUR NIFEMI", "ONWUCHEKWA FAVOUR", "ONYEMAECHI CHIZARALM E", 
    "ORUDIKE UGOCHI MARYJANE", "PATRICK SUNEBARI ANGEL", "PAUL FAVOUR GIFT", "RICHARD MIRABEL", 
    "SILAS MIRACLE AMARACHI", "SOLOMON ESE OGHENE ALICIA", "SUKA GLORY LERABARI", "SUNDAY MARY PRINCE", 
    "SUNDAY MIRACLE HANNAH", "THANKGOD FAVOUR", "TONAWA ELIZABETH", "UDOCHUKWU DIVINE OSINACHI", 
    "YEGIRA JOY", "YEREBA BEAUTY BARILE", "YODE PURITY"
]

# Folder where student PDF files are stored
file_path = "/Users/Adooz/JSS1APDF"  # Change this to your actual path

# Loop through each student and rename their corresponding file
for i, student in enumerate(students):
    # Create old and new filenames
    old_file = os.path.join(file_path, f"{student}.pdf")
    new_file = os.path.join(file_path, f"C2400{i + 1:02}.pdf")

    # Rename if file exists
    if os.path.exists(old_file):
        os.rename(old_file, new_file)
        print(f"Renamed '{old_file}' to '{new_file}'")
    else:
        print(f"File not found for: {student}")
