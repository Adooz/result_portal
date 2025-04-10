import os

# List of student names (this will be used to check the order of files)
students = [
    "ABEL PRAISE GOD", "AKIOMA BRIGHT", "AKPAN ESTHER KINGSLEY", "ALAUSA GIFT INIOLUWA",
    "AMOS ESTHER ALUWAYE", "ANTHONY REJOICE", "AUGUSTINE GOLD", "BARINE TOM GIFT",
    "BARITURE BARISIDO MIRIAM", "CHIGOZIE CHIZARAM", "CHIJIOKE DESIRE CHIOMA", "CHIKA BENITA",
    "CHIMA CHINASA CHRISTABEL", "CHRISTOPHER JULET OKON", "CYRIL ARCHIBONG DESTINY",
    "EDEM CHRISTIANA MICHAEL", "EMMANUEL CHUKWUCHIDERA", "EMMANUEL ESTHER UKO",
    "EMMANUEL UYIME DESIRE", "ENIWOAKE PRECIOUS", "ETIM DEBORAH LARRY", "ETUK PEACE SAMUEL",
    "EXOSE AFFADEYI", "FARUK SAADATU", "FRIDAY BARIMUE ESTHER", "FRIDAY GOODNEWS",
    "GODSWILL BRIGHTNESS", "IKECHUKWU REJOICE AMARACHI", "IMOH AWESOME BASSEY", "ITORO GLORY JAMES",
    "JACOB DESTINY", "JOSEPH SUNDAY FAITH", "JOSHUA MIRACLE IKOYO", "JUMBO BLESSING",
    "LEGBARA TAANABEBABARI", "MONDAY GOODNEWS", "MONDAY ROSEMARY", "NKEMAKOLAM MIRACLE",
    "NWAFOR VICTORY AMARACHI", "NWAWULU CHIKAMSO MARY ANN", "NWIGBARATO SALVATION S.K",
    "NZEDIEGWU CHRISTABEL", "OBOMANU MARVELLOUS G", "OHANAGOROM ROSEMARY", "OKAFOR DIVINE",
    "OLORUNDA AWOTUNDE HONOUR NIFEMI", "ONWUCHEKWA FAVOUR", "ONYEMAECHI CHIZARALM E",
    "ORUDIKE UGOCHI MARYJANE", "PATRICK SUNEBARI ANGEL", "PAUL FAVOUR GIFT", "RICHARD MIRABEL",
    "SILAS MIRACLE AMARACHI", "SOLOMON ESE OGHENE ALICIA", "SUKA GLORY LERABARI", "SUNDAY MARY PRINCE",
    "SUNDAY MIRACLE HANNAH", "THANKGOD FAVOUR", "TIMOTHY ABIGAIL", "TONAWA ELIZABETH",
    "UDOCHUKWU DIVINE OSINACHI", "UGBUNU FAVOUR OGHENENYERO", "YEGIRA JOY", "YEREBA BEAUTY BARILE",
    "YODE PURITY"
]

# Path where your files are stored
file_path = '/Users/Adooz/JSS1APDF'  # Change this to the directory containing student files

# Get all student files in the directory
files = os.listdir(file_path)

# Ensure the number of files matches the number of students
if len(files) == len(students):
    for i, file_name in enumerate(sorted(files)):  # Sorted to ensure the order is consistent
        # Creating the new file name (C240001, C240002, ...)
        new_name = f"C24000{i + 1:03}.pdf"  # Format to C240001, C240002, etc.

        # Define the full paths for renaming
        old_file_path = os.path.join(file_path, file_name)
        new_file_path = os.path.join(file_path, new_name)

        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{file_name}' to '{new_name}'")
else:
    print("The number of files does not match the number of students!")
