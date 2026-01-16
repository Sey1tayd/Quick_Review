from django.core.management.base import BaseCommand
from django.db.models import Max
from quiz.models import Course, Session, Question, Choice
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Adds questions for FIBA from CSV file'

    def handle(self, *args, **options):
        # Create or get course
        course, created = Course.objects.get_or_create(
            slug='fiba',
            defaults={'title': 'FIBA'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))
        else:
            self.stdout.write(f'Using existing course: {course.title}')

        # Create or get session
        session_title = 'Working question set'
        session_slug = slugify(session_title)
        session, created = Session.objects.get_or_create(
            course=course,
            slug=session_slug,
            defaults={'title': session_title, 'is_published': True}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created session: {session.title}'))
        else:
            self.stdout.write(f'Using existing session: {session.title}')

        # Questions data
        questions_data = [
            {
                'text': 'Madde 4 Takımlar | 4-1\nAçıklama: Takımdaki bütün oyuncuların forma ve şortun altına giydikleri dahil tüm kol ve bacak giyilebilir kompresyon malzemeleri, başörtüsü, bileklikleri, kafa-saç bantları aynı hakim renkte olmalıdır.\nÖrnek 4-2: Sahada A1 beyaz, A2 ise kırmızı saç bandı takar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A1 ve A2'nin farklı renkte saç bantları takmasına izin verilmez.",
                'choices': [
                    ('İzin verilmez', True),
                    ('izin verilir', False),
                ]
            },
            {
                'text': 'Madde 4 Takımlar | 4-1\nAçıklama: Takımdaki bütün oyuncuların forma ve şortun altına giydikleri dahil tüm kol ve bacak giyilebilir kompresyon malzemeleri, başörtüsü, bileklikleri, kafa-saç bantları aynı hakim renkte olmalıdır.\nÖrnek 4-3: Sahada A1 beyaz saç bandı, A2 ise kırmızı bileklik takar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Beyaz bir kafa bandı takan A1'e ve kırmızı bir bileklik takan A2'ye izin verilmez.",
                'choices': [
                    ('İzin verilmez', True),
                    ('izin verilir', False),
                ]
            },
            {
                'text': 'Madde 4 Takımlar | 4-4\nAçıklama: Fular tarzı kafa bantlarının takılmasına izin verilmez\nDiyagram Diyagram 1: Fular tarzı kafa bandı örnekleri\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '',
                'choices': [
                    ('İzin verilmez', True),
                    ('izin verilir', False),
                ]
            },
            {
                'text': 'Madde 4 Takımlar | 4-4\nAçıklama: Fular tarzı kafa bantlarının takılmasına izin verilmez\nÖrnek 4-5: A1, takım arkadaşlarının izin verilen diğer herhangi bir ek ekipmanıyla aynı hakim renkte fular tarzı bir kafa bandı takar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A1'in fular tarzı bir kafa bandı takmasına izin verilmez. Kafa bandı, başın etrafında açma /bağlama parçalarına sahip olmayacak ve üzerinde sıkmaya yarayacak herhangi bir parçası bulunmayacaktır.",
                'choices': [
                    ('İzin verilmez', True),
                    ('izin verilir', False),
                ]
            },
            {
                'text': 'Madde 4 Takımlar | 4-4\nAçıklama: Fular tarzı kafa bantlarının takılmasına izin verilmez\nÖrnek 4-6: A6, bir değişiklik talebinde bulunur. Hakemler A6’nın formasının altına kompresyon malzemesi özelliği olmayan bir tişört giydiğini fark ederler.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyuncu değişikliğine izin verilmez. Üniformanın altına sadece kompresyon malzemesi özelliği olan giysiler giyilebilir.',
                'choices': [
                    ('İzin verilmez', True),
                    ('izin verilir', False),
                ]
            },
            {
                'text': 'Madde 4 Takımlar | 4-4\nAçıklama: Fular tarzı kafa bantlarının takılmasına izin verilmez\nÖrnek 4-7: A6, şortunun altına aşağıda belirtilen şekilde kompresyon malzemesi özelliği olan bir giysi giyer. (a) Dizlerinin üzerine kadar uzayan, (b) Ayak bileklerine kadar uzayan.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Giyilebilir kompresyon malzemeleri (şort altına giyilen) kurallara uygundur ve herhangi bir uzunlukta giyilebilir. Takımdaki tüm oyuncular, forma ve şortun altına giydikleri dahil aynı hakim renkte kol ve bacak için giyilebilir kompresyon malzemeleri, başörtüsü, bileklik ve kafa-saç bantları kullanmalıdır.',
                'choices': [
                    ('Giyilebilir kompresyon malzemeleri (şort altına giyilen) kurallara uygundur ve herhangi bir uzunlukta giyilebilir. Takımdaki tüm oyuncular, forma ve şortun alt…', True),
                    ('Giyilebilir kompresyon malzemeleri (şort altına giyilen) kurallara uygun değildir ve herhangi bir uzunlukta giyilebilir. Takımdaki tüm oyuncular, forma ve şortun alt…', False),
                ]
            },
            {
                'text': 'Madde 4 Takımlar | 4-4\nAçıklama: Fular tarzı kafa bantlarının takılmasına izin verilmez\nÖrnek 4-8: A6, formasının altına aşağıda belirtilen şekilde kompresyon malzemesi özelliği olan bir atlet giyer. (a) Omuzlarının üzerine kadar uzayan, (b) Boynuna kadar uzayan.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Giyilebilir kompresyon malzemeleri (forma altına giyilen) kurallara uygundur ve kullanılabilir. (a) Omuzlarının üzerine ve altına doğru herhangi bir uzunlukta, (b) Boynun üst tarafına kadar uzayan Takımdaki tüm oyuncular, forma ve şortun altına giydikleri dahil aynı hakim renkte kol ve bacak için giyilebilir kompresyon malzemeleri, başörtüsü, bileklik ve kafa-saç bantları kullanmalıdır.',
                'choices': [
                    ('Giyilebilir kompresyon malzemeleri (forma altına giyilen) kurallara uygundur ve kullanılabilir. (a) Omuzlarının üzerine ve altına doğru herhangi bir uzunlukta,…', True),
                    ('Giyilebilir kompresyon malzemeleri (forma altına giyilen) kurallara uygun değildir ve kullanılabilir. (a) Omuzlarının üzerine ve altına doğru herhangi bir uzunlukta,…', False),
                ]
            },
            {
                'text': 'Madde 5 Sakatlanma ve yardım | 5-1\nAçıklama: Bir oyuncu sakatlanır ya da sakatlanmış görünür veya yardıma ihtiyacı olursa ve bunun sonucunda takımın sıra bölgesinde oturmasına izin verilen herhangi biri (aynı yakımın başantrenör, birinci yardımcı antrenör, yedek oyuncu, oyun dışı kalmış oyuncu ya da delegasyon üyesi) sahaya girerse, o oyuncunun gerçekten tedavi görüp görmediğine ya da yardım alıp almadığına bakılmaksızın tedavi olmuş veya yardım almış olarak kabul edilir.\nÖrnek 5-2: A1 ayak bile...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda A1 tedavi görmüş kabul edilir ve değiştirilecektir.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 5 Sakatlanma ve yardım | 5-1\nAçıklama: Bir oyuncu sakatlanır ya da sakatlanmış görünür veya yardıma ihtiyacı olursa ve bunun sonucunda takımın sıra bölgesinde oturmasına izin verilen herhangi biri (aynı yakımın başantrenör, birinci yardımcı antrenör, yedek oyuncu, oyun dışı kalmış oyuncu ya da delegasyon üyesi) sahaya girerse, o oyuncunun gerçekten tedavi görüp görmediğine ya da yardım alıp almadığına bakılmaksızın tedavi olmuş veya yardım almış olarak kabul edilir.\nÖrnek 5-3: Takımın fizy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1 bir yardım almıştır ve değiştirilecektir.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 5 Sakatlanma ve yardım | 5-1\nAçıklama: Bir oyuncu sakatlanır ya da sakatlanmış görünür veya yardıma ihtiyacı olursa ve bunun sonucunda takımın sıra bölgesinde oturmasına izin verilen herhangi biri (aynı yakımın başantrenör, birinci yardımcı antrenör, yedek oyuncu, oyun dışı kalmış oyuncu ya da delegasyon üyesi) sahaya girerse, o oyuncunun gerçekten tedavi görüp görmediğine ya da yardım alıp almadığına bakılmaksızın tedavi olmuş veya yardım almış olarak kabul edilir.\nÖrnek 5-4: Takımın dokt...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1 bir yardım almıştır ve değiştirilecektir.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': "Madde 5 Sakatlanma ve yardım | 5-5\nAçıklama: Takımının sıra bölgesinde oturmasına izin verilen herhangi bir kişi, takım sıra bölgesinde kalmaya devam ederken kendi takımındaki bir oyuncuya yardım edebilir. Eğer bu yardım oyunun hemen yeniden başlatılmasını geciktirmezse bu oyuncunun bir yardım almamış olduğu kabul edilir ve oyuncu değişikliği yapılmasını gerektirmez.\nÖrnek 5-6: B1, atış halindeki A1'e, A takımı sıra bölgesi alanı yakınında faul yapar. Top sepetten içeri girmez. A1, 2 ya da 3 ser...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Her iki durumda da A takımı oyuncusu, oyunun hemen yeniden başlatılmasını geciktiren bir yardım almamıştır. A takımı oyuncusu için oyuncu değişikliği yapılması gerekmeyecektir. A1, 2 ya da 3 serbest atışını atmaya devam edecektir.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': "Madde 5 Sakatlanma ve yardım | 5-5\nAçıklama: Takımının sıra bölgesinde oturmasına izin verilen herhangi bir kişi, takım sıra bölgesinde kalmaya devam ederken kendi takımındaki bir oyuncuya yardım edebilir. Eğer bu yardım oyunun hemen yeniden başlatılmasını geciktirmezse bu oyuncunun bir yardım almamış olduğu kabul edilir ve oyuncu değişikliği yapılmasını gerektirmez.\nÖrnek 5-7: B1, atış halindeki A1'e, A takımı sıra bölgesi alanı yakınında faul yapar. Top sepetten içeri girmez. Faulden sonra A1,...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'A1, oyunun hemen yeniden başlatılmasını geciktiren bir yardım almamıştır. A1 için oyuncu değişikliği yapılması gerekmeyecektir. A1, 2 ya da 3 serbest atış kullanacaktır.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': "Madde 5 Sakatlanma ve yardım | 5-5\nAçıklama: Takımının sıra bölgesinde oturmasına izin verilen herhangi bir kişi, takım sıra bölgesinde kalmaya devam ederken kendi takımındaki bir oyuncuya yardım edebilir. Eğer bu yardım oyunun hemen yeniden başlatılmasını geciktirmezse bu oyuncunun bir yardım almamış olduğu kabul edilir ve oyuncu değişikliği yapılmasını gerektirmez.\nÖrnek 5-8: A1'e 2 serbest atış hakkı verilir. Hakem faulü hakem masasına bildirirken A1 sahanın en uzağındaki takımının sıra bölge...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'A1, oyunun hemen yeniden başlatılmasını geciktiren bir yardım almamıştır. A1 için oyuncu değişikliği yapılması gerekmeyecektir. A1, 2 serbest atış kullanacaktır.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 5 Sakatlanma ve yardım | 5-5\nAçıklama: Takımının sıra bölgesinde oturmasına izin verilen herhangi bir kişi, takım sıra bölgesinde kalmaya devam ederken kendi takımındaki bir oyuncuya yardım edebilir. Eğer bu yardım oyunun hemen yeniden başlatılmasını geciktirmezse bu oyuncunun bir yardım almamış olduğu kabul edilir ve oyuncu değişikliği yapılmasını gerektirmez.\nÖrnek 5-9: A1 başarılı bir şut atar. Topu oyuna sokan B1, hakeme topun ıslak olduğunu gösterir. Hakem oyunu durdurur. B takımının ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da B1, oyunun hemen yeniden başlatılmasını geciktiren bir yardım almamıştır. B1 için oyuncu değişikliği yapılması gerekmeyecektir. Oyun, doğrudan arkalığın arkası hariç dip çizginin gerisindeki herhangi bir yerden B takımının topu oyuna sokmasıyla devam edecektir. Hakem, topu oyuna sokması için topu B takımı oyuncusuna verecektir.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 5 Sakatlanma ve yardım | 5-5\nAçıklama: Takımının sıra bölgesinde oturmasına izin verilen herhangi bir kişi, takım sıra bölgesinde kalmaya devam ederken kendi takımındaki bir oyuncuya yardım edebilir. Eğer bu yardım oyunun hemen yeniden başlatılmasını geciktirmezse bu oyuncunun bir yardım almamış olduğu kabul edilir ve oyuncu değişikliği yapılmasını gerektirmez.\nÖrnek 5-10: Top, kendi ön sahasından oyuna sokmak için A1’in ellerindedir. A takımı fizyoterapisti geri sahadaki takım sıra bölges...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A takımı fizyoterapisti A1'e, takım sıra bölgesi dışında bir yardım sağlamıştır. A1 için oyuncu değişikliği yapılması gerekecektir.",
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 5 Sakatlanma ve yardım | 5-5\nAçıklama: Takımının sıra bölgesinde oturmasına izin verilen herhangi bir kişi, takım sıra bölgesinde kalmaya devam ederken kendi takımındaki bir oyuncuya yardım edebilir. Eğer bu yardım oyunun hemen yeniden başlatılmasını geciktirmezse bu oyuncunun bir yardım almamış olduğu kabul edilir ve oyuncu değişikliği yapılmasını gerektirmez.\nÖrnek 5-11: Top, kendi ön sahasından oyuna sokmak için henüz A1’in ellerinde değildir. A takımı fizyoterapisti ön sahadaki kendi t...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A takımı fizyoterapisti, A1'e takım sıra bölgesi içinde bir yardım sağlamıştır. Yardım 15 saniye içinde tamamlanırsa A1'in değiştirilmesi gerekmez. Yardım 15 saniyeden fazla sürerse, A1 için oyuncu değişikliği yapılması gerekecektir.",
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 5 Sakatlanma ve yardım | 5-12\nAçıklama: Doktorun görüşüne göre sahada ciddi bir şekilde sakatlanan oyuncunun hareket ettirilmesi tehlikeliyse, sakatlanan oyuncunun sahadan çıkarılması için zaman limiti yoktur.\nÖrnek 5-13: A1, ciddi bir şekilde sakatlanır ve oyun 15 dakika kadar durur çünkü doktor, bu oyuncunun sahadan taşınmasının tehlikeli olacağını öngörmektedir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Sakatlanan oyuncunun sahadan ne zaman çıkarılacağını doktorun kararı belirleyecektir. Değişiklikten sonra oyun herhangi bir yaptırım uygulanmadan yeniden başlayacaktır.',
                'choices': [
                    ('Sakatlanan oyuncunun sahadan ne zaman çıkarılacağını doktorun kararı belirleyecektir. Değişiklikten sonra oyun herhangi bir yaptırım uygulanmadan yeniden başla…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 5 Sakatlanma ve yardım | 5-14\nAçıklama: Bir oyuncu sakatlanır ya da kanaması veya açık yarası olur ve oyuna hemen (yaklaşık 15saniye içinde) devam edemezse, ya da takım sıra bölgesinde oturmasına izin verilen herhangi biri tarafından kendisine yardım edilmişse, değiştirilmelidir. Aynı duran saat periyodunda takımlardan birisine bir mola verilirse ve bu mola sırasında bu oyuncu iyileşirse ya da yardım tamamlanırsa sayı görevlisi mola için sesli işaretini, hakemin bir yedek oyuncuyu, bir oyu...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Eğer A1, mola sırasında iyileşirse oynamaya devam edebilir. (b) A1’in yerine bir yedek oyuncu oyuna girmiştir bu nedenle A1, bir sonraki oyun saatinin çalışma periyodu bitene kadar tekrar giremez.',
                'choices': [
                    ('(a) Eğer A1, mola sırasında iyileşirse oynamaya devam edebilir. (b) A1’in yerine bir yedek oyuncu oyuna girmiştir bu nedenle A1, bir sonraki oyun saatinin çalı…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 5 Sakatlanma ve yardım | 5-16\nAçıklama: Başantrenörü tarafından oyuna başlayacağı belirtilen oyuncular bir sakatlık durumunda değiştirilebilirler. Bir sakatlık durumunda serbest atışlar arasında tedavi gören oyuncular değiştirilmelidir. Bu durumlarda rakipler de eğer isterlerse aynı sayıda oyuncu değiştirme hakkına sahiptirler.\nÖrnek 5-17: A1’e faul yapılır ve 2 serbest atış hakkı verilir. Birinci serbest atıştan sonra hakemler; (a) A1’de kanama tespit ederler ve A6 ile değiştirilir. B tak...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) B takımı sadece 1 oyuncu değiştirebilir. A6 ikinci serbest atışı kullanacaktır. (b) A takımı 1 oyuncu değiştirebilir. A1 ikinci serbest atışı kullanacaktır.',
                'choices': [
                    ('(a) B takımı sadece 1 oyuncu değiştirebilir. A6 ikinci serbest atışı kullanacaktır. (b) A takımı 1 oyuncu değiştirebilir. A1 ikinci serbest atışı kullanacaktır.', True),
                    ('1 serbest atış', False),
                    ('0 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 7 Başantrenör ve birinci yardımcı antrenör: Görevleri ve yetkileri | 7-1\nAçıklama: Maçın belirlenmiş başlama saatinden en az 40 dakika önce, her takımın başantrenörü ya da takımın temsilcisi sayı görevlisine oynayacak takım üyelerinin isimleri ve numaraları ile birlikte takım kaptanının, başantrenörün ve birinci yardımcı antrenörün isimlerini içeren bir liste verecektir. Başantrenör, oyuncuların formalarındaki numaraların listede doğru olduğundan kişisel olarak sorumludur. Maçın belirlenmi...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Herhangi bir yaptırım uygulanmadan yanlış numaralar düzeltilir ya da oyuncunun ismi maç kağıdına eklenir. (b) Hakem, her iki takımı dezavantajlı duruma düşürmeden uygun bir zamanda oyunu durdurur. Herhangi bir yaptırım uygulanmadan yanlış numaralar düzeltilir. Ancak, oyuncunun ismi maç kağıdına eklenemez.',
                'choices': [
                    ('(a) Herhangi bir yaptırım uygulanmadan yanlış numaralar düzeltilir ya da oyuncunun ismi maç kağıdına eklenir. (b) Hakem, her iki takımı dezavantajlı duruma düş…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 7 Başantrenör ve birinci yardımcı antrenör: Görevleri ve yetkileri | 7-1\nAçıklama: Maçın belirlenmiş başlama saatinden en az 40 dakika önce, her takımın başantrenörü ya da takımın temsilcisi sayı görevlisine oynayacak takım üyelerinin isimleri ve numaraları ile birlikte takım kaptanının, başantrenörün ve birinci yardımcı antrenörün isimlerini içeren bir liste verecektir. Başantrenör, oyuncuların formalarındaki numaraların listede doğru olduğundan kişisel olarak sorumludur. Maçın belirlenmi...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Takımlar, takım sırasında oturmasına izin verilen en fazla 8 delegasyon üyelerinin kimlerden oluşacağına karar verebilirler.',
                'choices': [
                    ('İzin verilir', True),
                    ('izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 7 Başantrenör ve birinci yardımcı antrenör: Görevleri ve yetkileri | 7-4\nAçıklama: Maçın belirlenmiş başlama saatinden en az 10 dakika önce, her takımın başantrenörü maça başlayacak olan 5 oyuncusunu belirtecektir. Maç başlamadan önce sayı görevlisi bu 5 oyuncuyla ilgili yanlışlık olup olmadığını kontrol edecek ve yanlışlık varsa, hemen en yakın hakemi bilgilendirecektir. Eğer hata, maçın başlamasından önce fark edilirse, ilk 5 başlayan oyuncular düzeltilecektir. Eğer hata, maçın başlaması...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Bu oyuncu, herhangi bir yaptırım olmadan, maça başlaması gereken 5 oyuncudan birisi ile değiştirilecektir. (b) Hata dikkate alınmaz. Maç herhangi bir cezai yaptırım olmadan devam eder.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 7 Başantrenör ve birinci yardımcı antrenör: Görevleri ve yetkileri | 7-4\nAçıklama: Maçın belirlenmiş başlama saatinden en az 10 dakika önce, her takımın başantrenörü maça başlayacak olan 5 oyuncusunu belirtecektir. Maç başlamadan önce sayı görevlisi bu 5 oyuncuyla ilgili yanlışlık olup olmadığını kontrol edecek ve yanlışlık varsa, hemen en yakın hakemi bilgilendirecektir. Eğer hata, maçın başlamasından önce fark edilirse, ilk 5 başlayan oyuncular düzeltilecektir. Eğer hata, maçın başlaması...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Başantrenör kişisel olarak maça başlayacak 5 oyuncusu için maç kağıdında ‘Giren oyuncu’ bölümündeki oyuncunun numarasının yanına küçük ‘x’ koyarak işaretleyecektir.',
                'choices': [
                    ('Başantrenör kişisel olarak maça başlayacak 5 oyuncusu için maç kağıdında ‘Giren oyuncu’ bölümündeki oyuncunun numarasının yanına küçük ‘x’ koyarak işaretleyece…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 7 Başantrenör ve birinci yardımcı antrenör: Görevleri ve yetkileri | 7-4\nAçıklama: Maçın belirlenmiş başlama saatinden en az 10 dakika önce, her takımın başantrenörü maça başlayacak olan 5 oyuncusunu belirtecektir. Maç başlamadan önce sayı görevlisi bu 5 oyuncuyla ilgili yanlışlık olup olmadığını kontrol edecek ve yanlışlık varsa, hemen en yakın hakemi bilgilendirecektir. Eğer hata, maçın başlamasından önce fark edilirse, ilk 5 başlayan oyuncular düzeltilecektir. Eğer hata, maçın başlaması...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A takımı kaptanı, A takımı oyuncu-başantrenörü olarak devam edecektir.',
                'choices': [
                    ('A takımı kaptanı, A takımı oyuncu-başantrenörü olarak devam edecektir.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 8 Oyun süresi, eşitlik ve uzatma | 8-1\nAçıklama: Oyun arası şu durumlarda başlar: • Oyunun belirlenmiş başlama saatinden 20 dakika önce. • Oyun saati, çeyreğin ya da uzatmanın sonu için sesli işaret verdiğinde. • Arkalığın çevresi kırmızı ışıkla donatıldığında ışık, oyun saatinin sesli işaretinden öncelikli olacaktır.\nÖrnek 8-2: B1, A1 atış halindeyken, oyun saati çeyreğin sonu için sesli işaretini vermeden önce faul yapar. (a) Başarısız bir şut girişimi sırasında (b) Başarılı bir şut giri...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "B1'in faulünün oyun saatinin çeyreğin sonu için sesli işareti vermesinden önce yapılıp yapılmadığı konusunda hakemler hemen birbirlerine danışacaklardır. B1'in faulünün oyun saati sesli işaretini vermeden önce olduğuna karar verirlerse B1’e bir kişisel faul verilecektir ve; (a) A1, 2 serbest atış kullanacaktır (b) A1’in sayısı geçerli sayılacak. A1, 1 serbest atış kullanacaktır. Oyun saati faulün yapıldığı zamana kadar olan süreye ayarlanacaktır. Oyun herhangi bir son serbest atıştan sonra olduğu gibi devam edecektir. B1'in faulünün oyun saati sesli işaretini verdikten sonra olduğuna karar verirlerse faul dikkate alınmayacaktır. Şut girişimi başarılı olmuşsa sayı geçerli sayılmayacaktır. Eğer B1'in faulü sportmenlik dışı veya diskalifiye edici faul kriterlerini karşılıyorsa ve sonrasında bir çeyrek veya uzatma oynanacaksa B1'in faulü göz ardı edilmeyecek ve buna göre cezası bir sonraki çeyrek ya da uzatma başlamadan önce uygulanacaktır. Faul, bir sonraki çeyrekte B takımının takım faulleri olarak sayılacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 8 Oyun süresi, eşitlik ve uzatma | 8-1\nAçıklama: Oyun arası şu durumlarda başlar: • Oyunun belirlenmiş başlama saatinden 20 dakika önce. • Oyun saati, çeyreğin ya da uzatmanın sonu için sesli işaret verdiğinde. • Arkalığın çevresi kırmızı ışıkla donatıldığında ışık, oyun saatinin sesli işaretinden öncelikli olacaktır.\nÖrnek 8-3: A1, 3 sayılık atış için bir şut girişiminde bulunur. Oyun saati oyunun sonu için sesli işaret verdiğinde top havadadır. Sesli işaretten sonra B1, hala havada olan ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A1'e 3 sayı verilecektir. B1'in A1'e yaptığı faul oyun süresinin bitiminden sonra meydana geldiği için, B1 tarafından yapılan faul sportmenlik dışı veya diskalifiye edici faul kriterlerini karşılamadığı sürece ve devamında başka bir çeyrek veya uzatma oynanmayacaksa dikkate alınmayacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 9 Bir çeyreğin, uzatmanın ya da oyunun başlaması ve sona ermesi | 9-1\nAçıklama: Maç, her bir takımın oyun sahasında oynama hakkı bulunan en az 5 oyuncu ile oynamaya hazır olmadıkça başlamayacaktır.\nÖrnek 9-2: İkinci devrenin başında A takımının sakatlıklar, diskalifiyeler, vb. nedenlerle sahada oynamaya hazır 5 oyuncusu bulunamaz.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'En az 5 oyuncu olma zorunluluğu sadece oyunun başında geçerlidir, A takımı 5’ten daha az oyuncu ile oynamaya devam edebilir.',
                'choices': [
                    ('En az 5 oyuncu olma zorunluluğu sadece oyunun başında geçerlidir, A takımı 5’ten daha az oyuncu ile oynamaya devam edebilir.', True),
                    ('En az 5 oyuncu olma zorunluluğu sadece oyunun başında geçerli değildir, A takımı 5’ten daha az oyuncu ile oynamaya devam edebilir.', False),
                ]
            },
            {
                'text': 'Madde 9 Bir çeyreğin, uzatmanın ya da oyunun başlaması ve sona ermesi | 9-1\nAçıklama: Maç, her bir takımın oyun sahasında oynama hakkı bulunan en az 5 oyuncu ile oynamaya hazır olmadıkça başlamayacaktır.\nÖrnek 9-3: Oyunun sonuna doğru A1, beşinci faulünü alır ve oyunu terk eder. A takımının başka bir yedek oyuncusu olmadığından sadece 4 oyuncusu kalmıştır. B takımı büyük bir sayı farkıyla önde olduğundan B takımı başantrenörü adil oyun adına, 4 oyuncuyla oynayarak devam etmek için bir oyuncusunu...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B takımı başantrenörünün 5’ten daha az oyuncuyla oynama isteği reddedilecektir. Bir takımın yeterli oyuncusu olduğu sürece sahada 5 oyuncusu olacaktır.',
                'choices': [
                    ('B takımı başantrenörünün 5’ten daha az oyuncuyla oynama isteği reddedilecektir. Bir takımın yeterli oyuncusu olduğu sürece sahada 5 oyuncusu olacaktır.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 9 Bir çeyreğin, uzatmanın ya da oyunun başlaması ve sona ermesi | 9-4\nAçıklama: Madde 9, bir takımın hangi sepeti savunacağını ve hangi sepete hücum edeceğini açıklar. Herhangi bir çeyrek ya da uzatma başında, iki takım karıştırarak yanlış sepetlere hücum/savunma yaparlarsa, bu durum fark edildiğinde her iki takım dezavantajlı duruma düşürülmeden hemen düzeltilecektir. Oyun durmadan önceki sayılar, geçen süre, yapılan fauller, vb. geçerli olur.\nÖrnek 9-5: Oyun başladıktan sonra hakemler, t...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun, herhangi bir takımı dezavantajlı duruma düşürmeden hemen durdurulacaktır. Takımlar oyunun yönünü düzelteceklerdir. Oyun, oyunun durdurduğu yere karşılık gelen yerin tam zıt tarafından devam edecektir.',
                'choices': [
                    ('Oyun, herhangi bir takımı dezavantajlı duruma düşürmeden hemen durdurulacaktır. Takımlar oyunun yönünü düzelteceklerdir. Oyun, oyunun durdurduğu yere karşılık …', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 9 Bir çeyreğin, uzatmanın ya da oyunun başlaması ve sona ermesi | 9-6\nAçıklama: Oyun, orta dairede yapılacak bir hava atışıyla başlayacaktır.\nÖrnek 9-7: Maç öncesi oyun arası sırasında A1’e bir teknik faul verilir. Maç başlamadan önce B takımı başantrenörü B6’nın 1 serbest atış atacağını belirtir ancak B6, takımın oyuna başlayacak 5 oyuncusundan birisi değildir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Sadece B takımının oyuna başlayacak 5 oyuncusundan birisi, kimse dizilmeden serbest atışı kullanacaktır. Oyun saati başlamadan önce değişikliğe izin verilmez. Oyun bir hava atışı ile başlayacaktır.',
                'choices': [
                    ('İzin verilmez', True),
                    ('izin verilir', False),
                ]
            },
            {
                'text': 'Madde 9 Bir çeyreğin, uzatmanın ya da oyunun başlaması ve sona ermesi | 9-6\nAçıklama: Oyun, orta dairede yapılacak bir hava atışıyla başlayacaktır.\nÖrnek 9-8: Maç öncesi oyun arası sırasında A1, B1’e bir sportmenlik dışı faul yapar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Maç başlamadan önce, B1 kimse dizilmeden 2 serbest atış kullanacaktır. Eğer B1 oyuna başlayacak 5 oyuncudan birisi olarak belirtilmişse B1 sahada kalacaktır. Eğer B1 oyuna başlayacak 5 oyuncudan birisi olarak belirtilmemişse B1 sahada kalmayacaktır. Oyun bir hava atışı ile başlayacaktır.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 9 Bir çeyreğin, uzatmanın ya da oyunun başlaması ve sona ermesi | 9-9\nAçıklama: Maçtan önceki oyun arası sırasında, oyuna başlayacak ilk 5 oyuncudan biri olarak belirlenen bir oyuncu oyuna başlayamaz veya oyuna başlama hakkını yitirirse başka bir oyuncu ile değiştirilecektir. Bu durumda rakipler isterlerse, oyuna başlayacak ilk 5 oyuncusundan bir oyuncuyu değiştirme hakkına sahiptir.\nÖrnek 9-10: A1, A takımının oyuna başlayacak ilk 5 oyuncusundan biridir. Maçtan 7 dakika önce, oyun arası s...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da A1, başka bir A takımı oyuncusu ile değiştirilecektir. Bu durumda B takımı isterse oyuna başlayacak ilk 5 oyuncusundan birini değiştirme hakkına sahiptir.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 10 Topun statüsü | 10-1\nAçıklama: Bir oyuncu atış halinde olduğunda ve savunma takımının bir oyuncusu şut girişimindeki oyuncunun devam eden hareketi başladıktan sonra herhangi bir rakibe bir faul yaptığında, atış halinde olan oyuncu devam eden hareketiyle şut girişimini tamamladığında top ölmez ve sayı olmuşsa geçerli sayılır. Bu açıklama, savunma takımının bir oyuncusuna veya takım sıra bölgesinde oturmaya izinli herhangi bir kişiye bir teknik faul verilmesinde de aynı şekilde geçerlidir...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da A1’in atışı başarılı olursa sayı geçerli olacaktır. (a) Oyun, B2 tarafından yapılan faulün meydana geldiği en yakın yerden A takımının topu oyuna sokmasıyla devam edecektir. (b) A2, 2 serbest atış kullanacaktır. Oyun herhangi bir son serbest atıştan sonra olduğu gibi devam edecektir.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 10 Topun statüsü | 10-1\nAçıklama: Bir oyuncu atış halinde olduğunda ve savunma takımının bir oyuncusu şut girişimindeki oyuncunun devam eden hareketi başladıktan sonra herhangi bir rakibe bir faul yaptığında, atış halinde olan oyuncu devam eden hareketiyle şut girişimini tamamladığında top ölmez ve sayı olmuşsa geçerli sayılır. Bu açıklama, savunma takımının bir oyuncusuna veya takım sıra bölgesinde oturmaya izinli herhangi bir kişiye bir teknik faul verilmesinde de aynı şekilde geçerlidir...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A2’ye bir takım kontrolü faulü verildiğinde top ölür. Eğer A1'in şutu başarılı olursa, sayı geçerli sayılmayacaktır. A takımının bu çeyrekteki faul sayısına bakılmaksızın oyun, serbest atış çizgisi uzantısından B takımının topu oyuna sokmasıyla devam edecektir. Eğer A1’in şutu başarısız olursa oyun, doğrudan arkalığın arkası hariç faulün meydana geldiği en yakın yerden B takımının topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': "Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-2: Oyunun başlamasından iki dakika önce A1'e bir teknik faul verilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'B takımının oyuna başlayacak olan 5 oyuncusundan birisi, kimse dizilmeden serbest atış kullanacaktır. Oyun henüz başlamadığından, pozisyon sırası okunun yönü herhangi bir takımı gösteremez. Oyun, bir hava atışı ile başlayacaktır.',
                'choices': [
                    ('B takımının oyuna başlayacak olan 5 oyuncusundan birisi, kimse dizilmeden serbest atış kullanacaktır. Oyun henüz başlamadığından, pozisyon sırası okunun yönü h…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-3: Başhakem, başlama hava atışı için topu atar. Top en yüksek noktaya ulaşmadan önce hava atışına sıçrayan A1 topa temas eder.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu, A1 tarafından yapılan bir hava atışı ihlalidir. B takımına kendi ön sahasından, orta çizgiye en yakın yerinden topu oyuna sokma hakkı verilecektir. B takımının şut saatinde 14 saniyesi olacaktır. Top, B takımının topu oyuna sokacak olan oyuncusunun kullanımına verilir verilmez, A takımı bir sonraki pozisyon sırasına göre topu oyuna sokma hakkına sahip olacaktır.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-4: Başhakem, başlama hava atışı için topu atar. Top en yüksek noktaya ulaşmadan önce hava atışına katılmayan A2; (a) geri sahasından (b) ön sahasından orta daireye girer.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da A2 hava atışı ihlali yapmıştır. B takımına orta çizginin ihlalin olduğu en yakın yerinden topu oyuna sokma hakkı verilecektir. (a) ön sahasındaysa, şut saatinde 14 saniye ile (b) geri sahasındaysa, şut saatinde 24 saniye ile Top, B takımının topu oyuna sokacak olan oyuncusunun kullanımına verilir verilmez, A takımı bir sonraki pozisyon sırasına göre topu oyuna sokma hakkına sahip olacaktır.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-5: Başhakem ,başlama hava atışı için topu atar. Top hava atışına sıçrayan A1 tarafından kurallara uygun olarak tiplendikten hemen sonra; (a) A2 ve B2 arasında bir tutulmuş top kararı verilir. (b) A2...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da canlı bir topun kontrolü henüz oluşmadığından hakemler pozisyon sırası prosedürünü kullanamazlar. Başhakem, orta dairede başka bir hava atışı yapacak ve buna A2 ile B2 katılacaktır. Topun kurallara uygun olarak tiplenmesinden sonra ve tutulmuş top/çift faul meydana gelmeden önce oyun saatinde geçen süre geçerli kalacaktır.',
                'choices': [
                    ('Tutulmuş top', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-6: Başhakem ,başlama hava atışı için topu atar. Top hava atışına sıçrayan A1 tarafından kurallara uygun olarak tiplendikten hemen sonra top; (a) Doğrudan saha dışına gider. (b) Hava atışına çıkmayan...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da A1’in ihlali sonucunda B takımına topu oyuna sokma hakkı verilir. B takımı tarafından topun oyuna sokulması geri sahadan yönetilecekse, şut saatinde 24 saniyesi, ön sahadan yönetilecekse şut saatinde 14 saniyesi olacaktır. Top, B takımının topu oyuna sokacak olan oyuncusunun kullanımına verilir verilmez, A takımı bir sonraki pozisyon sırasına göre topu oyuna sokma hakkına sahip olacaktır.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': "Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-7: Başhakem, başlama hava atışı için topu atar. Top hava atışına sıçrayan A1 tarafından kurallara uygun olarak tiplendikten hemen sonra B1'e bir teknik faul verilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Bir A takımı oyuncusu serbest atış için topu alır almaz, pozisyon sırası okunun yönü B takımını gösterecektir. Oyun, teknik faul meydana geldiğinde topun bulunduğu yere en yakın yerden B takımının topu oyuna sokmasıyla devam edecektir. Topun oyuna sokulması B takımının geri sahasındansa, B takımının şut saatinde 24 saniyesi olacaktır. Topun oyuna sokulması B takımının ön sahasındansa, B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-8: Başhakem, başlama hava atışı için topu atar. Top hava atışına sıçrayan A1 tarafından kurallara uygun olarak tiplendikten hemen sonra B2’ye yaptığı bir temas sebebiyle A2’ye sportmenlik dışı bir f...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B2, kimse dizilmeden 2 serbest atış kullanacaktır. B2, ilk serbest atış için topu alır almaz pozisyon sırası okunun yönü A takımının gösterecektir. Oyun, B takımının ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir (sportmenlik dışı faul cezasının bir parçası olarak). B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-9: Pozisyon sırası prosedürüne göre B takımı topu oyuna sokma hakkına sahiptir. Bir hakem ve/veya sayı görevlisi hata yapar ve top oyuna sokulması için yanlışlıkla A takımına verilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Top, bir kez sahadaki bir oyuncuya temas ettiğinde ya da sahadaki bir oyuncu tarafından kurallara uygun olarak topa temas edildiğinde hata düzeltilemez. Ancak B takımı yanlışlık sonucunda bir sonraki hava atışı durumunda pozisyon sırasına göre oyuna sokma hakkını kaybetmeyecektir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-10: Birinci çeyreğin sonu için oyun saatinin sesli işaretiyle aynı anda B1, A1'e bir sportmenlik dışı faul yapar. Hakemler, oyun saatinin sesli işaretinin B1'in faulü gerçekleşmeden önce çaldığına k...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Sportmenlik dışı faul oyun arasında meydana gelmiştir. İkinci çeyreğe başlamadan önce A1, kimse dizilmeden 2 serbest atış kullanacaktır. Oyun, A takımının ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır. A takımı, bir sonraki hava atışı durumunda pozisyon sırasına göre topu oyuna sokma hakkını kaybetmeyecektir.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-11: Oyun saati, üçüncü çeyreğin sonu için sesli işareti vermesinden hemen sonra B1’e teknik faul verilir. A takımı dördüncü çeyreğin başında topu oyuna sokmak için pozisyon sırası hakkına sahiptir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Herhangi bir A takım oyuncusu, dördüncü çeyrek başlamadan önce kimse dizilmeden 1 serbest atış kullanacaktır. Dördüncü çeyrek, A takımının orta çizgi uzantısından topu oyuna sokmasıyla başlayacaktır. A takımının şut saatinde 24 saniye olacaktır.',
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-12: A1 top ellerindeyken sıçrar ve B1 tarafından kurallara uygun olarak kendisine blok yapılır. Her iki oyuncu daha sonra, her ikisinin de bir ya da iki eli sıkıca topun üzerinde olacak şekilde saha...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu bir hava atışı durumudur.',
                'choices': [
                    ('Bu bir hava atışı durumudur.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-13: : A1 top ellerindeyken sıçrar ve B1 tarafından kurallara uygun olarak kendisine blok yapılır. Daha sonra A1 bir ya da iki eli sıkıca topun üzerinde olacak şekilde sahaya geri döndüğünde B1 artık...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A1 tarafından yapılan bir yürüme ihlalidir.',
                'choices': [
                    ('Yürüme ihlali (top kaybı)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-14: A1 ve B1 havadayken, elleri sıkıca topun üzerindedir. Oyun sahasına döndükten sonra A1, bir ayağıyla sınır çizgisine üzerine iner.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu bir hava atışı durumudur.',
                'choices': [
                    ('Bu bir hava atışı durumudur.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-1\nAçıklama: Oyunun başlangıcındaki hava atışından sonra canlı bir topun ilk takım kontrolünü sağlayamayan takıma, doğrudan arkalığın arkası hariç, bir sonraki hava atışı durumunun meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.\nÖrnek 12-15: A1, top ellerindeyken kendi ön sahasından sıçrar ve kendisine B1 tarafından kurallara uygun olarak blok yapılır. Her iki oyuncu daha sonra, her ikisinin de bir ya da iki eli sıkıca topun üzerind...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu bir hava atışı durumudur.',
                'choices': [
                    ('Bu bir hava atışı durumudur.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-16\nAçıklama: Serbest atışlar arası olmadıkça ve son serbest atıştan sonra faul cezasının parçası olan topu oyuna sokma hakkı olmadıkça canlı bir top çemberle arkalık arasına sıkıştığında bu, pozisyon sırasına göre topun oyuna sokulmasıyla sonuçlanan bir hava atışı durumudur. Şut saati, pozisyon sırası prosedürüne göre hücum takımı topu oyuna sokma hakkına sahipse 14 saniyeye ya da savunma takımı topu oyuna sokma hakkına sahipse 24 saniyeye ayarlanacakt...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Top, kendi dip çizgisinin gerisinden oyuna sokulduktan sonra şut saatinde: (a) A takımının 14 saniyesi, (b) B takımının 24 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-16\nAçıklama: Serbest atışlar arası olmadıkça ve son serbest atıştan sonra faul cezasının parçası olan topu oyuna sokma hakkı olmadıkça canlı bir top çemberle arkalık arasına sıkıştığında bu, pozisyon sırasına göre topun oyuna sokulmasıyla sonuçlanan bir hava atışı durumudur. Şut saati, pozisyon sırası prosedürüne göre hücum takımı topu oyuna sokma hakkına sahipse 14 saniyeye ya da savunma takımı topu oyuna sokma hakkına sahipse 24 saniyeye ayarlanacakt...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu bir hava atışı durumudur. Top, kendi dip çizgisinin gerisinden oyuna sokulduktan sonra A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-16\nAçıklama: Serbest atışlar arası olmadıkça ve son serbest atıştan sonra faul cezasının parçası olan topu oyuna sokma hakkı olmadıkça canlı bir top çemberle arkalık arasına sıkıştığında bu, pozisyon sırasına göre topun oyuna sokulmasıyla sonuçlanan bir hava atışı durumudur. Şut saati, pozisyon sırası prosedürüne göre hücum takımı topu oyuna sokma hakkına sahipse 14 saniyeye ya da savunma takımı topu oyuna sokma hakkına sahipse 24 saniyeye ayarlanacakt...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda serbest atış başarısız olarak dikkate alınacaktır. Oyun, A takımının ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-16\nAçıklama: Serbest atışlar arası olmadıkça ve son serbest atıştan sonra faul cezasının parçası olan topu oyuna sokma hakkı olmadıkça canlı bir top çemberle arkalık arasına sıkıştığında bu, pozisyon sırasına göre topun oyuna sokulmasıyla sonuçlanan bir hava atışı durumudur. Şut saati, pozisyon sırası prosedürüne göre hücum takımı topu oyuna sokma hakkına sahipse 14 saniyeye ya da savunma takımı topu oyuna sokma hakkına sahipse 24 saniyeye ayarlanacakt...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu bir hava atışı durumudur. Pozisyon sırası okunun yönü hemen B takımına çevrilecektir. Oyun, B takımı tarafından, doğrudan arkalığın arkası hariç kendi dip çizgisinin gerisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-16\nAçıklama: Serbest atışlar arası olmadıkça ve son serbest atıştan sonra faul cezasının parçası olan topu oyuna sokma hakkı olmadıkça canlı bir top çemberle arkalık arasına sıkıştığında bu, pozisyon sırasına göre topun oyuna sokulmasıyla sonuçlanan bir hava atışı durumudur. Şut saati, pozisyon sırası prosedürüne göre hücum takımı topu oyuna sokma hakkına sahipse 14 saniyeye ya da savunma takımı topu oyuna sokma hakkına sahipse 24 saniyeye ayarlanacakt...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu bir hava atışı durumudur. Oyun A takımı tarafından, doğrudan arkalığın arkası hariç ön sahasındaki dip çizginin gerisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır. A takımının topu oyuna sokması tamamlanınca pozisyon sırası okunun yönü hemen çevrilecektir.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-22\nAçıklama: Rakip takımlardan bir ya da daha fazla oyuncunun bir veya her iki eli sıkıca topun üzerinde olduğunda, hiçbir oyuncunu aşırı güç harcamadan topun kontrolünü elde edemediğinde tutulmuş top durumu oluşur.\nÖrnek 12-23: A1’in sayı yapmak amacıyla sepete doğru devam eden hareketinde top ellerindedir. Bu sırada B1 ellerini sıkıca topun üzerine koyar ve bu anda A1, yürüme kuralında izin verilenden daha fazla adım atar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu bir hava atışı durumudur.',
                'choices': [
                    ('Bu bir hava atışı durumudur.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 12 Hava atışı ve pozisyon sırası | 12-24\nAçıklama: Pozisyon sırasına göre top oyuna sokulurken yapılan bir ihlal, o takımın pozisyon sırasına göre topu oyuna sokmasını kaybetmesine neden olur.\nÖrnek 12-25: Bir çeyrekte oyun saatinde 4:17 kala pozisyon sırasına göre top oyuna sokulduğu sırada: (a) Topu oyuna sokacak olan A1 top el ya da ellerindeyken sahaya adım atar. (b) Top, sınır çizgisinden oyuna sokulmadan önce A2 sınır çizgisi üzerinden ellerini uzatır. (c) Topu oyuna sokacak olan A1,...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda bu, A1 ya da A2 tarafından topun oyuna sokulması sırasında yapılan bir ihlaldir. Oyun, orijinal topu oyuna sokma yerinden B takımı tarafından topun oyuna sokulmasıyla devam edecektir. Pozisyon sırası okunun yönü hemen B takımına çevrilecektir.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': "Madde 12 Hava atışı ve pozisyon sırası | 12-26\nAçıklama: Bir hava atışı durumu meydana geldiğinde eğer şut saatinde kalan süre bulunmuyorsa ve pozisyon sırası oku A takımını gösteriyorsa pozisyon değiştirme prosedürü uygulanmayacaktır. Bu bir şut saati ihlalidir. Bu nedenle top, oyuna sokması için B takımına verilecektir.\nÖrnek 12-27: A1'in başarısız bir şut girişimi sırasında top havadayken şut saati sesli işaret verir. Daha sonra; (a) Bir tutulmuş top durumu oluşur (b) Bir teknik faul verilir....\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': '',
                'choices': [
                    ('Tutulmuş top', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "Madde 12 Hava atışı ve pozisyon sırası | 12-26\nAçıklama: Bir hava atışı durumu meydana geldiğinde eğer şut saatinde kalan süre bulunmuyorsa ve pozisyon sırası oku A takımını gösteriyorsa pozisyon değiştirme prosedürü uygulanmayacaktır. Bu bir şut saati ihlalidir. Bu nedenle top, oyuna sokması için B takımına verilecektir.\nÖrnek 12-28: A1'in sayı amacıyla bir şut girişimi sırasında top havadayken şut saati sesli işaret verir. Top çembere değmez. Daha sonra; (a) A1 ya da B1'e bir teknik faul veril...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': '',
                'choices': [
                    ('Tutulmuş top', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 13 Topla nasıl oynanır | 13-1\nAçıklama: Oyun sırasın top sadece el ya da ellerle oynanır. Bir oyuncunun kurallara aykırı olarak; • bir pas ya da şut aldatması yapmak için topu bacaklarının arasına koyması, • topla oynamak için kasıtlı olarak kafasını, yumruğunu, bacaklarını ya da ayaklarını kullanması bir ihlaldir.\nÖrnek 13-2: A1 driplingini bitirir. A1 topu bacaklarının arasına koyar ve pas ya da şut aldatması yapar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu, A1 tarafından topa kurallara aykırı olarak bacağıyla dokunmasından dolayı yapılan bir ihlaldir.',
                'choices': [
                    ('Bu, A1 tarafından topa kurallara aykırı olarak bacağıyla dokunmasından dolayı yapılan bir ihlaldir.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "Madde 13 Topla nasıl oynanır | 13-1\nAçıklama: Oyun sırasın top sadece el ya da ellerle oynanır. Bir oyuncunun kurallara aykırı olarak; • bir pas ya da şut aldatması yapmak için topu bacaklarının arasına koyması, • topla oynamak için kasıtlı olarak kafasını, yumruğunu, bacaklarını ya da ayaklarını kullanması bir ihlaldir.\nÖrnek 13-3: A1, hızlı hücum sırasında rakibin sepetine doğru koşmakta olan A2'ye topu pas olarak atar. A2, topu yakalamadan önce kasıtlı olarak kafasıyla topa dokunur.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Bu, kurallara aykırı olarak kafasını kullanarak topla oynayan A2 tarafından yapılmış bir ihlaldir.',
                'choices': [
                    ('Bu, kurallara aykırı olarak kafasını kullanarak topla oynayan A2 tarafından yapılmış bir ihlaldir.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "Madde 13 Topla nasıl oynanır | 13-4\nAçıklama: Bir oyuncunun boyunun ya da uzanabileceği/erişebileceği yerin artırılmasına izin verilmez. Bir takım arkadaşını topla oynaması için kaldırmak bir ihlaldir.\nÖrnek 13-5: A1, takım arkadaşı A2'yi rakibin sepeti altında kucaklar ve kaldırır. A3, sepete smaç yapması için topu A2'ye pas olarak atar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Bu, A takımı tarafından yapılan bir ihlaldir. A2’nin sayısı geçerli sayılmayacaktır. Oyun, geri sahasındaki serbest atış çizgisi uzantısından B takımının topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 14 Topun kontrolü | 14-1\nAçıklama: Takım kontrolü, o takımdan bir oyuncunun canlı bir topu tutarak, dripling yaparak ya da topu oyuna sokmak veya serbest atış için canlı bir topu kullanımına almasıyla başlar.\nÖrnek 14-2: Oyun saatinin durdurulup ya da durdurulmadığına bakılmaksızın, hakemin değerlendirmesine göre bir oyuncu bilerek topun oyuna sokulmasını ya da serbest atış için topu alma işlemini kasıtlı olarak geciktirir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Hakem topu, topun oyuna sokulacağı yerin yakınına ya da serbest atış çizgisine sahaya koyduğunda top canlanır ve takım kontrolü başlar.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 14 Topun kontrolü | 14-1\nAçıklama: Takım kontrolü, o takımdan bir oyuncunun canlı bir topu tutarak, dripling yaparak ya da topu oyuna sokmak veya serbest atış için canlı bir topu kullanımına almasıyla başlar.\nÖrnek 14-3: A takımı topu 15 saniye kontrol etmiştir. A1 topu A2’ye pas olarak atar ve havadaki top sınır çizgisi üzerinden geçer. B1, sahadan sınır çizgisinin üzerine doğru sıçrayarak topu yakalamaya çalışır. B1 hala havadayken top B1’in, (a) bir ya da her iki eliyle tiplenir, (b) he...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) A takımı topu kontrol etmeye devam eder. A takımının şut saatinde kalan süresi kadar zamanı olacaktır. (b) B1, B takımı için top kontrolünü kazanmıştır. Sonrasında A takımı, A2 ile tekrardan topun kontrolü kazanmıştır. A takımının şut saatinde yeni bir 24 saniyesi olacaktır.',
                'choices': [
                    ('(a) A takımı topu kontrol etmeye devam eder. A takımının şut saatinde kalan süresi kadar zamanı olacaktır. (b) B1, B takımı için top kontrolünü kazanmıştır. So…', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': "Madde 15 Atış halindeki oyuncu | 15-1\nAçıklama: Bir şut durumunda atış hali, hakemin değerlendirmesine göre oyuncunun topu, rakibinin sepetine doğru yukarıya doğru hareket ettirmesiyle başlar.\nÖrnek 15-2: A1 sepete doğru hareket ederken, topu yukarı doğru hareket ettirmeden her iki ayağı sahadayken kurallara uygun olarak durur. Bu sırada B1, A1'e faul yapar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'A1 henüz topu, sepete doğru yukarı hareket ettirmeye başlamadığından, B1’in faulü atış halindeki bir oyuncuya yapılmamıştır.',
                'choices': [
                    ('A1 henüz topu, sepete doğru yukarı hareket ettirmeye başlamadığından, B1’in faulü atış halindeki bir oyuncuya yapılmamıştır.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "Madde 15 Atış halindeki oyuncu | 15-3\nAçıklama: Potaya doğru devam eden hareketlerdeki atış hali, dripling tamamlanarak top oyuncunun el ya da ellerinde durduğunda veya havada tutulduğunda ve hakemin değerlendirmesine göre oyuncunun sahadan atış için topun el veya ellerini terk etmesinden önce şut hareketine başladığında başlar.\nÖrnek 15-4: A1 potaya doğru yüklenirken elinde topla driplingini bitirir ve şut hareketine başlar. Bu sırada B1, A1'e faul yapar. Top sepetten içeri girmez.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "B1'in faulü, atış halindeki bir oyuncuya yapılmıştır. A1, 2 serbest atış kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir.",
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': "Madde 15 Atış halindeki oyuncu | 15-3\nAçıklama: Potaya doğru devam eden hareketlerdeki atış hali, dripling tamamlanarak top oyuncunun el ya da ellerinde durduğunda veya havada tutulduğunda ve hakemin değerlendirmesine göre oyuncunun sahadan atış için topun el veya ellerini terk etmesinden önce şut hareketine başladığında başlar.\nÖrnek 15-5: A1 havaya sıçrar ve 3 sayılık atış girişimi için topu ellerinden çıkarır. B1, A1'e her iki ayağıyla oyun sahasına dönmeden önce faul yapar. Top sepetten içer...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'A1, her iki ayağıyla oyun sahasına dönene kadar atış halindedir. A1, 3 serbest atış kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir.',
                'choices': [
                    ('3 serbest atış', True),
                    ('2 serbest atış', False),
                    ('1 serbest atış', False),
                ]
            },
            {
                'text': "Madde 15 Atış halindeki oyuncu | 15-3\nAçıklama: Potaya doğru devam eden hareketlerdeki atış hali, dripling tamamlanarak top oyuncunun el ya da ellerinde durduğunda veya havada tutulduğunda ve hakemin değerlendirmesine göre oyuncunun sahadan atış için topun el veya ellerini terk etmesinden önce şut hareketine başladığında başlar.\nÖrnek 15-6: A1 ön sahada topu tutarken B1'e faul yapar. Bu bir takım kontrol faulüdür. A1 ileri doğru devam hareketinde topu sepetten içeri atar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'A1’in sayısı geçerli sayılmaz. B takımına kendi geri sahasındaki serbest atış çizgisinin uzantısından topu oyuna sokma hakkı verilecektir.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 15 Atış halindeki oyuncu | 15-3\nAçıklama: Potaya doğru devam eden hareketlerdeki atış hali, dripling tamamlanarak top oyuncunun el ya da ellerinde durduğunda veya havada tutulduğunda ve hakemin değerlendirmesine göre oyuncunun sahadan atış için topun el veya ellerini terk etmesinden önce şut hareketine başladığında başlar.\nÖrnek 15-7: A1, sepete doğru hareketlendiği ve ön ayağı hala sahadayken kendisine B1 tarafından faul yapılır. A1 atış hali durumuna devam eder ve B1’in kendisine yaptığı...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "B1'in faulü, A1 atış halindeyken meydana gelmiştir. Top bir an için A1'in ellerini terk ettiğinde, topun kontrolü hala A1 de aynen kalır ve bundan dolayı atış hali devam eder. Sayı geçerli sayılır. A1, 1 serbest atış kullanacaktır. Oyun herhangi bir son serbest atıştan sonra olduğu gibi devam edecektir.",
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 15 Atış halindeki oyuncu | 15-8\nAçıklama: Bir oyuncu atış halindeyken ve kendisine faul yapıldıktan sonra topu pas olarak atarsa, bu oyuncu artık atış halinde olarak kabul edilmez.\nÖrnek 15-9: B1 atış halindeki A1’e faul yapar. Bu, B takımının o çeyrekteki 3. takım faulüdür. Faulden sonra A1, A2’ye pas verir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A1 topu A2'ye pas olarak verdiğinde atış hali sona ermiştir. Oyun A takımı tarafından, faulün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 15 Atış halindeki oyuncu | 15-10\nAçıklama: Bir oyuncuya atış halindeyken faul yapılırsa ve bunun ardından bu oyuncu bir yürüme ihlali yaparak sayı yaparsa,sayı geçerli sayılmaz ve 2 ya da 3 serbest atış hakkı verilir.\nÖrnek 15-11: Top A1’in ellerinden 2 sayılık atış girişimi için sepete doğru hareket eder. B1, A1’e faul yapar, ardından A1 bir yürüme ihlali yapar. Top sepetten içeri girer.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A1’in sayısı geçerli sayılmaz. A1'e 2 serbest atış hakkı verilecektir.",
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 16 Sayı yapıldığı zaman ve değeri | 16-1\nAçıklama: Sahadan yapılan bir sayının değeri, şutun elden çıktığı sahadaki yere göre belirlenir. 2 sayı bölgesinden atılan bir şut 2 sayı, 3 sayı bölgesinden atılan bir şut 3 sayı olarak sayılır. Sahadan yapılan bir atış, topun girmiş olduğu rakiplerinin sepetine hücum eden takıma yazılır.\nÖrnek 16-2: A1, sahanın 3 sayı bölgesinden bir şut atar. Top havada yükselirken A takımının 2 sayı bölgesi içerisinde olan herhangi bir oyuncu tarafından kurallar...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in şutu, sahanın 3 sayı bölgesinden elden çıktığı için A takımına 3 sayı verilecektir.',
                'choices': [
                    ('A1’in şutu, sahanın 3 sayı bölgesinden elden çıktığı için A takımına 3 sayı verilecektir.', True),
                    ('A1’in şutu, sahanın 3 sayı bölgesinden elden çıktığı için A takımına 3 sayı verilmeyecektir.', False),
                ]
            },
            {
                'text': 'Madde 16 Sayı yapıldığı zaman ve değeri | 16-1\nAçıklama: Sahadan yapılan bir sayının değeri, şutun elden çıktığı sahadaki yere göre belirlenir. 2 sayı bölgesinden atılan bir şut 2 sayı, 3 sayı bölgesinden atılan bir şut 3 sayı olarak sayılır. Sahadan yapılan bir atış, topun girmiş olduğu rakiplerinin sepetine hücum eden takıma yazılır.\nÖrnek 16-3: A1, sahanın 2 sayı bölgesinden bir şut atar. Top havada yükselirken, A takımının 3 sayı bölgesinden sıçrayan B1, kurallara uygun olarak topa temas ede...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in şutu sahanın 2 sayı bölgesinden elden çıktığı için A takımına 2 sayı verilecektir.',
                'choices': [
                    ('A1’in şutu sahanın 2 sayı bölgesinden elden çıktığı için A takımına 2 sayı verilecektir.', True),
                    ('A1’in şutu sahanın 2 sayı bölgesinden elden çıktığı için A takımına 2 sayı verilmeyecektir.', False),
                ]
            },
            {
                'text': 'Madde 16 Sayı yapıldığı zaman ve değeri | 16-1\nAçıklama: Sahadan yapılan bir sayının değeri, şutun elden çıktığı sahadaki yere göre belirlenir. 2 sayı bölgesinden atılan bir şut 2 sayı, 3 sayı bölgesinden atılan bir şut 3 sayı olarak sayılır. Sahadan yapılan bir atış, topun girmiş olduğu rakiplerinin sepetine hücum eden takıma yazılır.\nÖrnek 16-4: Bir çeyreğin başında A takımı kendi sepetini savunurken B1 yanlışlıkla kendi sepetine dripling yapar ve sayı atar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A takımının sahadaki kaptanına 2 sayı yazılır.',
                'choices': [
                    ('A takımının sahadaki kaptanına 2 sayı yazılır.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 16 Sayı yapıldığı zaman ve değeri | 16-5\nAçıklama: Top rakibin sepetine girerse, sahadan yapılan atışın değeri topun sahada elden çıktığı yere göre belirlenir. Top doğrudan ya da dolaylı olarak sepete girebilir veya bir pas sırasında top sepete girmeden önce herhangi bir oyuncuya veya sahaya temas edebilir.\nÖrnek 16-6: A1, sahanın 3 sayı bölgesinden topu pas olarak atar. (a) Top doğrudan sepetten içeri girer. (b) Top sahanın 2 sayı ya da 3 sayı bölgesindeki herhangi bir oyuncuya temas eder...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da A1’in pası, sahanın 3 sayılık bölgesinden elden çıktığı için A takımına 3 sayı verilecektir.',
                'choices': [
                    ('Her iki durumda da A1’in pası, sahanın 3 sayılık bölgesinden elden çıktığı için A takımına 3 sayı verilecektir.', True),
                    ('Her iki durumda da A1’in pası, sahanın 3 sayılık bölgesinden elden çıktığı için A takımına 3 sayı verilmeyecektir.', False),
                ]
            },
            {
                'text': "Madde 16 Sayı yapıldığı zaman ve değeri | 16-5\nAçıklama: Top rakibin sepetine girerse, sahadan yapılan atışın değeri topun sahada elden çıktığı yere göre belirlenir. Top doğrudan ya da dolaylı olarak sepete girebilir veya bir pas sırasında top sepete girmeden önce herhangi bir oyuncuya veya sahaya temas edebilir.\nÖrnek 16-7: A1, 3 sayı bölgesinden bir şut girişiminde bulunur. Top A1'in ellerini terk ettikten sonra A takımının 2 sayı bölgesindeki sahaya temas eder. Top sepetten içeri girer.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "A1'in atışı, 3 sayı bölgesinde elden çıktığı için 3 sayı olarak sayılacaktır. Oyun, herhangi bir başarılı atış sonrasında olduğu gibi devam edecektir.",
                'choices': [
                    ("A1'in atışı, 3 sayı bölgesinde elden çıktığı için 3 sayı olarak sayılacaktır. Oyun, herhangi bir başarılı atış sonrasında olduğu gibi devam edecektir.", True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "Madde 16 Sayı yapıldığı zaman ve değeri | 16-5\nAçıklama: Top rakibin sepetine girerse, sahadan yapılan atışın değeri topun sahada elden çıktığı yere göre belirlenir. Top doğrudan ya da dolaylı olarak sepete girebilir veya bir pas sırasında top sepete girmeden önce herhangi bir oyuncuya veya sahaya temas edebilir.\nÖrnek 16-8: B1, 3 sayılık şut için atış halindeki A1'e faul yapar. Top sahaya temas eder ve ardından sepetten içeri girer.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'A1’in sayısı geçerli sayılmaz. Sahadan yapılan bu şut girişimi, top sahaya temas ettiğinde sona erer. Bir hakem düdüğünü çaldıktan sonra ve top artık sahadan atılan bir şut durumunda olmadığından, top anında ölür. A1, 3 serbest atış kullanacaktır.',
                'choices': [
                    ('3 serbest atış', True),
                    ('2 serbest atış', False),
                    ('1 serbest atış', False),
                ]
            },
            {
                'text': "Madde 16 Sayı yapıldığı zaman ve değeri | 16-5\nAçıklama: Top rakibin sepetine girerse, sahadan yapılan atışın değeri topun sahada elden çıktığı yere göre belirlenir. Top doğrudan ya da dolaylı olarak sepete girebilir veya bir pas sırasında top sepete girmeden önce herhangi bir oyuncuya veya sahaya temas edebilir.\nÖrnek 16-9: A1, 3 sayı bölgesinden bir şut girişiminde bulunur. Top, A1'in ellerinden çıktıktan sonra oyun saati çeyreğin sonu için sesli işaret verir. Top sahaya temas eder ve ardından...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'A1’in atışı geçerli sayılmaz. Sahadan yapılan bir şut girişimi, top oyun sahasına temas ettiğinde sona erer. Bir hakem düdüğünü çaldıktan sonra ve top artık sahadan atılan bir şut durumunda olmadığından oyun saati çeyreğin sonu için sesli işaret verdiğinde top ölür.',
                'choices': [
                    ('A1’in atışı geçerli sayılmaz. Sahadan yapılan bir şut girişimi, top oyun sahasına temas ettiğinde sona erer. Bir hakem düdüğünü çaldıktan sonra ve top artık sa…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 16 Sayı yapıldığı zaman ve değeri | 16-10\nAçıklama: Bir topu oyuna sokma durumunda ya da son serbest atış sonrası ribaund durumunda saha içindeki oyuncunun topa temas etmesinden, topun o oyuncunun elinden şut için çıkmasına kadar daima bir zaman periyodu vardır. Buna, çeyreğin ya da uzatmanın sonuna doğru dikkat edilmesi özellikle önemlidir. Zaman bitmeden önce bir şut atmak için minimum bir uygun süre olmalıdır. Oyun saati ya da şut saati 0:00.3 saniye gösteriyorsa, oyuncunun çeyrek ve uz...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Hakemler kalan oyun süresinin, doğru bir şekilde oyun ve şut saatinde gösterilmesini sağlayacaklardır. (a) Sahadan bir şut girişimi sırasında, oyun saati ya da şut saati çeyrek ya da uzatmanın sonu için sesli işaret verirse topun, oyun saati ya da şut saati çeyrek ya da uzatma için sesli işaret vermeden önce elden çıkıp çıkmadığını belirlemek hakemlerin sorumluluğundadır. (b) Sahadan yapılan bir atış sadece, top oyuna sokulurken atılan pas sonucunda top havadayken sepete tiplenirse ya da doğrudan sepetin içine smaç yapılırsa sayı verilebilir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 16 Sayı yapıldığı zaman ve değeri | 16-10\nAçıklama: Bir topu oyuna sokma durumunda ya da son serbest atış sonrası ribaund durumunda saha içindeki oyuncunun topa temas etmesinden, topun o oyuncunun elinden şut için çıkmasına kadar daima bir zaman periyodu vardır. Buna, çeyreğin ya da uzatmanın sonuna doğru dikkat edilmesi özellikle önemlidir. Zaman bitmeden önce bir şut atmak için minimum bir uygun süre olmalıdır. Oyun saati ya da şut saati 0:00.3 saniye gösteriyorsa, oyuncunun çeyrek ve uz...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Oyun saati çeyreğin sonu için sesli işaret verdiğinde top hala A1'in el ya da ellerine temas ettiğinden, A1’in sayısı geçerli sayılmayacaktır.",
                'choices': [
                    ("Oyun saati çeyreğin sonu için sesli işaret verdiğinde top hala A1'in el ya da ellerine temas ettiğinden, A1’in sayısı geçerli sayılmayacaktır.", True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 16 Sayı yapıldığı zaman ve değeri | 16-13\nAçıklama: Canlı bir top sepete üstten girdiğinde ve içinde kaldığında ya da tümüyle sepetten geçtiğinde sayı olur. (a) Bir savunma takımı, oyunun herhangi bir anında bir mola ister ve sonrasında sayı olur, ya da (b) Oyun saati dördüncü çeyrek ya da uzatmada 2:00 dakika ya da daha az gösterdiğinde,\nDiyagram Diyagram 2: ’de gösterildiği gibi, top sepetin içinde kaldığında ya da tamamen sepetten geçtiğinde oyun saati durdurulacaktır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '',
                'choices': [
                    ('Oyun saati durdurulur', True),
                    ('Oyun saati devam eder', False),
                ]
            },
            {
                'text': 'Madde 16 Sayı yapıldığı zaman ve değeri | 16-13\nAçıklama: Canlı bir top sepete üstten girdiğinde ve içinde kaldığında ya da tümüyle sepetten geçtiğinde sayı olur. (a) Bir savunma takımı, oyunun herhangi bir anında bir mola ister ve sonrasında sayı olur, ya da (b) Oyun saati dördüncü çeyrek ya da uzatmada 2:00 dakika ya da daha az gösterdiğinde,\nDiyagram Diyagram 2: Sayı\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '',
                'choices': [
                    ('Açıklama: Canlı bir top sepete üstten girdiğinde ve içinde kaldığında ya da tümüyle sepetten geçtiğinde sayı olur. (a) Bir savunma takımı, oyunun herhangi bir …', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 16 Sayı yapıldığı zaman ve değeri | 16-13\nAçıklama: Canlı bir top sepete üstten girdiğinde ve içinde kaldığında ya da tümüyle sepetten geçtiğinde sayı olur. (a) Bir savunma takımı, oyunun herhangi bir anında bir mola ister ve sonrasında sayı olur, ya da (b) Oyun saati dördüncü çeyrek ya da uzatmada 2:00 dakika ya da daha az gösterdiğinde,\nÖrnek 16-14: Dördüncü çeyrekte oyun saatinde 2:02 kala A1 başarılı bir şut girişiminde bulunur ve top sepetin içinden geçer. Oyun saatinde 2:00 kala B1 d...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Sayı, oyun saatinde 2:00'den fazla süre varken atılmıştır. Bu nedenle oyun saati durdurulmayacaktır.",
                'choices': [
                    ('Oyun saati durdurulur', True),
                    ('Oyun saati devam eder', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-1\nAçıklama: Topun oyuna sokulması sırasında topu oyuna sokan oyuncu dışındaki diğer oyuncuların vücutlarının herhangi bir kısmı sınır çizgisi üzerinde olmayacaktır. Topu oyuna sokacak oyuncunun, topu elinden çıkartmadan önce topun oyuna sokulması hareketi, oyuncunun el ya da ellerinin topla birlikte saha içi alanını saha dışı alanından ayrı tutan sınır çizgisinin üzerinden geçmesine neden olabilir. Bu gibi durumlarda top, oyuna sokacak oyuncunun ellerinde oldu...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da B1, topun oyuna sokulmasına müdahale etmiştir, bu nedenle oyun gecikmiştir. Hakem oyunun gecikmesinden dolayı ihlal kakarı verir. Ayrıca, B1’e sözlü bir uyarı verilir ve bu durum B takımı başantrenörüne de bildirilir. Bu uyarı oyunun geride kalan bölümünde B takımının tüm oyuncuları için geçerli olacaktır. B takımının herhangi bir oyuncusunun benzer bir hareketi tekrarlaması, teknik faulle sonuçlanabilir. A takımı tarafından topun oyuna sokulması tekrarlanacaktır. A takımının şut saatinde 24 saniye süresi olacaktır.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-1\nAçıklama: Topun oyuna sokulması sırasında topu oyuna sokan oyuncu dışındaki diğer oyuncuların vücutlarının herhangi bir kısmı sınır çizgisi üzerinde olmayacaktır. Topu oyuna sokacak oyuncunun, topu elinden çıkartmadan önce topun oyuna sokulması hareketi, oyuncunun el ya da ellerinin topla birlikte saha içi alanını saha dışı alanından ayrı tutan sınır çizgisinin üzerinden geçmesine neden olabilir. Bu gibi durumlarda top, oyuna sokacak oyuncunun ellerinde oldu...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Bu B1'in, top oyuna sokulurken yaptığı bir ihlaldir. Ayrıca, B1’e sözlü bir uyarı verilir ve bu durum B takımı başantrenörüne de bildirilir. Bu uyarı oyunun geride kalan bölümünde B takımının tüm oyuncuları için geçerli olacaktır. B takımının herhangi bir oyuncusunun benzer bir hareketi tekrarlaması, teknik faulle sonuçlanabilir. A takımının topu oyuna sokması tekrarlanacaktır. A takımının şut saatinde; (a) 14 saniyesi (b) 17 saniyesi olacaktır.",
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-4\nAçıklama: Oyun saati dördüncü çeyrekte ve her uzatmada 2:00 dakika ya da daha az gösterirken topun oyuna sokulması sırasında savunma takımının oyuncusu, topun oyuna sokulmasına müdahale etmek için vücudunun hiçbir bölümünü sınır çizgisi üzerinde hareket ettirmeyecektir.\nÖrnek 17-5: Dördüncü çeyrekte oyun saatinde 54 saniye kala A takımı topu oyuna sokma hakkına sahiptir. Hakem topu oyuna sokacak olan A1’in kullanımına vermeden önce B1’e “kural dışı sınır çiz...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B1’e bir teknik faul verilecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-4\nAçıklama: Oyun saati dördüncü çeyrekte ve her uzatmada 2:00 dakika ya da daha az gösterirken topun oyuna sokulması sırasında savunma takımının oyuncusu, topun oyuna sokulmasına müdahale etmek için vücudunun hiçbir bölümünü sınır çizgisi üzerinde hareket ettirmeyecektir.\nÖrnek 17-6: Dördüncü çeyrekte oyun saatinde 51 saniye kala A takımı topu oyuna sokma hakkına sahiptir. Hakem topu oyuna sokacak olan A1’in kullanımına vermeden önce B1’e “kural dışı sınır çiz...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Hakem B1’e “kural dışı sınır çizgisini geçme” uyarı işaretini göstermediğinden dolayı düdüğünü çalacak ve B1'e bir uyarı verilecektir. Bu uyarı aynı zamanda B takımı başantrenörüne de iletilecektir. Bu uyarı oyunun geri kalanındaki benzer durumlar için tüm B takımı oyuncuları için geçerli olacaktır. Herhangi bir B takımı oyuncusu tarafından benzer hareketin tekrarı teknik faulle sonuçlanabilir. Topun oyuna sokulması tekrarlanacak ve hakem “kural dışı sınır çizgisini geçme” uyarı işaretini gösterecektir.",
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': "Madde 17 Topun oyuna sokulması | 17-7\nAçıklama: Top oyuna sokulurken, oyuna sokan oyuncu topu sahadaki takım arkadaşına pas olarak vermelidir (elden ele değil).\nÖrnek 17-8: Topu oyuna sokan A1, topu sahadaki A2'ye elden ele verir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'A1, topu oyuna sokma ihlali yapmıştır. Topun oyuna sokulmasının sırasında top, oyuna sokacak oyuncunun el ya da ellerini terk etmelidir. B takımına orijinal topu oyuna sokma yerinden topu oyuna sokma hakkı verilecektir.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-9\nAçıklama: Topun oyuna sokulması sırasında başka bir oyuncu ya da oyuncuların vücutlarının herhangi bir kısmı top sahaya geçmeden önce sınır çizgisinin üzerinde olmayacaktır.\nÖrnek 17-10: Bir ihlal sonrasında topu oyuna sokacak olan A1 topu hakemden alır ve: (a) topu zemine koyar ve sonrasında A2 topu alır. (b) saha dışındaki A2’ye elden ele pas verir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da bu, A1 topu sınır çizgisinin diğer tarafına atmadan önce vücudunu sınır çizgisi üzerinde hareket ettirdiği için A2’nin ihlalidir.',
                'choices': [
                    ('Her iki durumda da bu, A1 topu sınır çizgisinin diğer tarafına atmadan önce vücudunu sınır çizgisi üzerinde hareket ettirdiği için A2’nin ihlalidir.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-9\nAçıklama: Topun oyuna sokulması sırasında başka bir oyuncu ya da oyuncuların vücutlarının herhangi bir kısmı top sahaya geçmeden önce sınır çizgisinin üzerinde olmayacaktır.\nÖrnek 17-11: A takımı tarafından sahadan yapılan başarılı bir atıştan ya da başarılı son serbest atıştan sonra B takımına mola verilir. Mola sonrasında B1, dip çizgide topu oyuna sokmak için topu hakemden alır. B1 daha sonra: (a) Topu zemine koyar ve ardından top, yine dip çizginin geris...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da bu, B2 tarafından kurallara uygun bir oyundur, B takımı için tek kısıtlama, oyuncularının topu sahaya 5 saniye içinde atmak zorunda olmalarıdır.',
                'choices': [
                    ('Her iki durumda da bu, B2 tarafından kurallara uygun bir oyundur, B takımı için tek kısıtlama, oyuncularının topu sahaya 5 saniye içinde atmak zorunda olmaları…', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-12\nAçıklama: Oyun saati dördüncü çeyrekte ya da her uzatmada 2:00 dakika veya daha az gösterdiğinde, geri sahasında topa sahip olma hakkı olan takıma bir mola verilirse, mola sonrasında başantrenör, topun oyuna sokulmasının takımının ön sahasındaki topu oyuna sokma çizgisinden ya da takımının geri sahasından yönetileceğine karar verme hakkına sahiptir. Başantrenör kararını verdikten sonra bu kesindir ve geri alınamaz. Aynı duran saat periyodundaki diğer molala...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'En geç moladan sonra başhakem, A takım başantrenörüne topun oyuna sokulmasının nereden yönetileceği ile ilgili kararını soracaktır. A takımı başantrenörü İngilizce (ya da Türkçe) dilinde yüksek sesle ‘frontcourt’ (ön saha) ya da ‘backcourt’ (geri saha) olarak söyleyecek ve aynı zamanda topun oyuna sokulmasının yönetileceği yeri (ön saha ya da geri saha) koluyla gösterecektir. A takımı başantrenörünün kararı kesindir ve geri alınamaz. Başhakem, A takımı başantrenörünün kararını, B takımı başantrenörüne bildirecektir. Oyun ancak, her iki takımın sahadaki oyuncuları tarafından oyunun nereden devam edeceği açıkça anlaşıldığında A takımının topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-12\nAçıklama: Oyun saati dördüncü çeyrekte ya da her uzatmada 2:00 dakika veya daha az gösterdiğinde, geri sahasında topa sahip olma hakkı olan takıma bir mola verilirse, mola sonrasında başantrenör, topun oyuna sokulmasının takımının ön sahasındaki topu oyuna sokma çizgisinden ya da takımının geri sahasından yönetileceğine karar verme hakkına sahiptir. Başantrenör kararını verdikten sonra bu kesindir ve geri alınamaz. Aynı duran saat periyodundaki diğer molala...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Oyun, A takımının geri sahasındaki serbest atış çizgisi uzantısından topu sokmasıyla devam edecektir. A takımının şut saatinde 17 saniyesi olacaktır. (b) ve (c) A takımı başantrenörü topun oyuna sokulması için kendi ön sahasına karar verirse oyun, A takımının ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır. A takımı başantrenörü topun geri sahasından oyuna sokulmasına karar verirse, A takımının şut saatinde 17 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-12\nAçıklama: Oyun saati dördüncü çeyrekte ya da her uzatmada 2:00 dakika veya daha az gösterdiğinde, geri sahasında topa sahip olma hakkı olan takıma bir mola verilirse, mola sonrasında başantrenör, topun oyuna sokulmasının takımının ön sahasındaki topu oyuna sokma çizgisinden ya da takımının geri sahasından yönetileceğine karar verme hakkına sahiptir. Başantrenör kararını verdikten sonra bu kesindir ve geri alınamaz. Aynı duran saat periyodundaki diğer molala...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Moladan sonra B takımı başantrenörü, oyunun devamı için topun oyuna sokulmasına: (a) Ön sahasındaki topun oyuna sokulması çizgisinden karar verirse B takımının şut saatinde 14 saniyesi olacaktır. (b) Geri sahasından karar verirse B takımının şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-12\nAçıklama: Oyun saati dördüncü çeyrekte ya da her uzatmada 2:00 dakika veya daha az gösterdiğinde, geri sahasında topa sahip olma hakkı olan takıma bir mola verilirse, mola sonrasında başantrenör, topun oyuna sokulmasının takımının ön sahasındaki topu oyuna sokma çizgisinden ya da takımının geri sahasından yönetileceğine karar verme hakkına sahiptir. Başantrenör kararını verdikten sonra bu kesindir ve geri alınamaz. Aynı duran saat periyodundaki diğer molala...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Moladan sonra: A takımı başantrenörü topun oyuna sokulması için takımının ön sahasındaki topu oyuna sokma çizgisine karar verirse, her iki durumda da A takımının şut saatinde 14 saniyesi olacaktır. A takımı başantrenörü topun oyuna sokulması için takımının geri sahasına karar verirse A takımının şut saatinde: (a) 18 saniyesi, (b) 24 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-12\nAçıklama: Oyun saati dördüncü çeyrekte ya da her uzatmada 2:00 dakika veya daha az gösterdiğinde, geri sahasında topa sahip olma hakkı olan takıma bir mola verilirse, mola sonrasında başantrenör, topun oyuna sokulmasının takımının ön sahasındaki topu oyuna sokma çizgisinden ya da takımının geri sahasından yönetileceğine karar verme hakkına sahiptir. Başantrenör kararını verdikten sonra bu kesindir ve geri alınamaz. Aynı duran saat periyodundaki diğer molala...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Moladan sonra: A takımı başantrenörü topun oyuna sokulması için takımının ön sahasındaki topu oyuna sokma çizgisine karar verirse, A takımının şut saatinde: (a) 6 saniyesi, (b) 14 saniyesi olacaktır. A takımı başantrenörü topun oyuna sokulması için takımının geri sahasına karar verirse, A takımının şut saatinde: (a) 6 saniyesi, (b) 17 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-12\nAçıklama: Oyun saati dördüncü çeyrekte ya da her uzatmada 2:00 dakika veya daha az gösterdiğinde, geri sahasında topa sahip olma hakkı olan takıma bir mola verilirse, mola sonrasında başantrenör, topun oyuna sokulmasının takımının ön sahasındaki topu oyuna sokma çizgisinden ya da takımının geri sahasından yönetileceğine karar verme hakkına sahiptir. Başantrenör kararını verdikten sonra bu kesindir ve geri alınamaz. Aynı duran saat periyodundaki diğer molala...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da mola sonrasında A takımı başantrenörü topun oyuna sokulması için takımının ön sahasındaki topu oyuna sokma çizgisine karar verirse, her iki durumda da A takımının şut saatinde 14 saniyesi olacaktır. A takımı başantrenörü topun oyuna sokulması için takımının geri sahasına karar verirse, her iki durumda da A takımının şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-12\nAçıklama: Oyun saati dördüncü çeyrekte ya da her uzatmada 2:00 dakika veya daha az gösterdiğinde, geri sahasında topa sahip olma hakkı olan takıma bir mola verilirse, mola sonrasında başantrenör, topun oyuna sokulmasının takımının ön sahasındaki topu oyuna sokma çizgisinden ya da takımının geri sahasından yönetileceğine karar verme hakkına sahiptir. Başantrenör kararını verdikten sonra bu kesindir ve geri alınamaz. Aynı duran saat periyodundaki diğer molala...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Diskalifiye edici faul cezaları birbirini götürür. Oyun A takımı tarafından, geri sahasından topu oyuna sokmasıyla devam edecektir. Ancak moladan sonra A takımı başantrenörü ön sahasından topun oyuna sokulmasına karar verirse, A takımının şut saatinde 14 saniyesi olacaktır. A takımı başantrenörü geri sahasından topun oyuna sokulmasına karar verirse, A takımının şut saatinde 19 saniyesi olacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-12\nAçıklama: Oyun saati dördüncü çeyrekte ya da her uzatmada 2:00 dakika veya daha az gösterdiğinde, geri sahasında topa sahip olma hakkı olan takıma bir mola verilirse, mola sonrasında başantrenör, topun oyuna sokulmasının takımının ön sahasındaki topu oyuna sokma çizgisinden ya da takımının geri sahasından yönetileceğine karar verme hakkına sahiptir. Başantrenör kararını verdikten sonra bu kesindir ve geri alınamaz. Aynı duran saat periyodundaki diğer molala...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Diskalifiye edici faul cezaları birbirini götürür. Mola sonrasında oyun A takımı tarafından, ön sahasından, kavga başladığında topun olduğu en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 19 saniyesi olacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-12\nAçıklama: Oyun saati dördüncü çeyrekte ya da her uzatmada 2:00 dakika veya daha az gösterdiğinde, geri sahasında topa sahip olma hakkı olan takıma bir mola verilirse, mola sonrasında başantrenör, topun oyuna sokulmasının takımının ön sahasındaki topu oyuna sokma çizgisinden ya da takımının geri sahasından yönetileceğine karar verme hakkına sahiptir. Başantrenör kararını verdikten sonra bu kesindir ve geri alınamaz. Aynı duran saat periyodundaki diğer molala...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A takımı başantrenörünün topun oyuna sokulmasının kendi ön sahasından yönetilmesi kararı kesindir ve geri alınamaz. Bu aynı zamanda, birinci mola sonrasında A takımı başantrenörünün ikinci bir mola almasında da geçerlidir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-22\nAçıklama: Birinci çeyrek hariç tüm çeyreklerin ve tüm uzatmaların başında topun oyuna sokulması, hakem masasının karşısındaki orta çizgi uzantısından yönetilecektir. Topu oyuna sokacak oyuncu birer ayağını orta çizginin iki yanına koyacaktır. Oyuna sokacak oyuncu bir ihlal yaparsa top, orta çizgi uzantısından oyuna sokması için rakiplere verilecektir. Ancak sahanın doğrudan orta çizgisi üzerinde bir kural ihlali olursa, topun oyuna sokulması orta çizgiye en...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun, oyun saatinde 10:00 ve şut saatinde 24 saniye olmak üzere, orta çizgi uzantısındaki orijinal topu oyuna sokma yerinden, B takımının topu oyuna sokmasıyla devam edecektir. Topu oyuna sokacak oyuncu, topu sahanın herhangi bir yerine pas atma hakkına sahip olacaktır. Pozisyon sırası okunun yönü B takımına çevrilecektir.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-22\nAçıklama: Birinci çeyrek hariç tüm çeyreklerin ve tüm uzatmaların başında topun oyuna sokulması, hakem masasının karşısındaki orta çizgi uzantısından yönetilecektir. Topu oyuna sokacak oyuncu birer ayağını orta çizginin iki yanına koyacaktır. Oyuna sokacak oyuncu bir ihlal yaparsa top, orta çizgi uzantısından oyuna sokması için rakiplere verilecektir. Ancak sahanın doğrudan orta çizgisi üzerinde bir kural ihlali olursa, topun oyuna sokulması orta çizgiye en...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun, B takımı tarafından, topun saha dışına çıktığı en yakın yerden topu oyuna sokmasıyla devam edecektir: (a) Geri sahasında şut saatinde 24 saniyeyle (b) Ön sahasında şu saatinde 14 saniyeyle. A2 topa temas ettiğinde A takımının topu oyuna sokması sona erer. Pozisyon sırası okunun yönü, B takımına çevrilecektir.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-22\nAçıklama: Birinci çeyrek hariç tüm çeyreklerin ve tüm uzatmaların başında topun oyuna sokulması, hakem masasının karşısındaki orta çizgi uzantısından yönetilecektir. Topu oyuna sokacak oyuncu birer ayağını orta çizginin iki yanına koyacaktır. Oyuna sokacak oyuncu bir ihlal yaparsa top, orta çizgi uzantısından oyuna sokması için rakiplere verilecektir. Ancak sahanın doğrudan orta çizgisi üzerinde bir kural ihlali olursa, topun oyuna sokulması orta çizgiye en...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda oyun, ön sahanın orta çizgiye en yakın yerinden B takımının topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-26\nAçıklama: Bir sportmenlik dışı ya da diskalifiye edici faul sonrasında topun oyuna sokulması, her zaman o takımın ön sahasındaki topu oyuna sokma çizgisinden yönetilecektir.\nÖrnek 17-27: Birinci ve ikinci çeyrek arasındaki oyun arası sırasında A1, B1’e sportmenlik dışı faul yapar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'İkinci çeyrek başlamadan önce B1, kimse dizilmeden 2 serbest atış kullanacaktır. Oyun, B takımının ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır. Pozisyon sırası ok yönü değişmeden kalacaktır.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-28\nAçıklama: Top oyuna sokulması sırasında aşağıdaki durumlar meydana gelebilir. (a) Top sepetin üzerine doğru pas olarak atılır ve herhangi bir takımın oyuncusu tarafından sepete doğru alttan uzanılarak topa temas edilir. Bu bir topa müdahale ihlalidir. (b) Top, çemberle arkalık arasına sıkışır. Bu bir hava atışı durumudur.\nÖrnek 17-29: Topu oyuna sokan A1 topu sepetin üzerine doğru atar ve herhangi bir takımın oyuncusu tarafından sepete doğru alttan uzanılar...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu bir müdahale ihlaldir. Oyun, rakipler tarafından serbest atış çizgisi uzantısından topun oyuna sokulmasıyla devam edecektir. Savunma takımı ihlal yaparsa top saha dışından geldiği için hücum takımına sayı verilmeyecektir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-28\nAçıklama: Top oyuna sokulması sırasında aşağıdaki durumlar meydana gelebilir. (a) Top sepetin üzerine doğru pas olarak atılır ve herhangi bir takımın oyuncusu tarafından sepete doğru alttan uzanılarak topa temas edilir. Bu bir topa müdahale ihlalidir. (b) Top, çemberle arkalık arasına sıkışır. Bu bir hava atışı durumudur.\nÖrnek 17-30: Topu oyuna sokan A1, topu B takımının sepetine doğru pas olarak atar ve top çemberle arkalık arasında sıkışır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu bir hava atışı durumudur. Oyun, pozisyon sırası prosedürü uygulanarak devam edecektir: • A takımı topu oyuna sokma hakkına sahipse oyun, A takımı tarafından ön sahasındaki dip çizgiden, arkalığın dorudan arkası hariç en yakın yerden topun oyuna sokulmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır. • B takımı topu oyuna sokma hakkına sahipse oyun, B takımı tarafından geri sahasındaki dip çizgiden, arkalığın dorudan arkası hariç en yakın yerden topun oyuna sokulmasıyla devam edecektir. B takımının şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-31\nAçıklama: Top kenardan oyuna sokacak olan oyuncunun kullanımında olduktan sonra bu oyuncu, başka bir oyuncu topa değmeden ya da oyun alanı içerisinde top, başka bir oyuncuya temas etmeden önce topu saha içerisine sektirerek tekrar temas edemez.\nÖrnek 17-32: Topu oyuna sokan A1 topu sektirir ve top: (a) Saha içine (b) Saha dışına temas eder ve sonra A1 topu tekrar yakalar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) A1, topu oyuna sokma ihlali yapmıştır. Top, A1’in el ya ellerini terk ettikten ve saha içine temas ettikten sonra A1, top sahadaki herhangi bir oyuncuya ya da sahadaki herhangi bir oyuncu topa temas etmeden önce topa temas etmeyecektir. (b) Eğer A1, topun sektiği yer ile topu tekrar yakaladığı yer arasında toplamda 1 metreden fazla hareket etmediyse bu durum kurallara uygundur ve topu elinden çıkarması için 5 saniye sayılmaya devam edilir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-33\nAçıklama: Topu oyuna sokan oyuncu, topun oyuna sokulması sırasında top elinden çıktıktan sonra, topun saha dışına temas etmesine neden olmayacaktır.\nÖrnek 17-34: Topu oyuna sokan A1, topu kendi (a) Ön sahasından, (b) Geri sahasından saha içerisindeki A2’ye pas atar. Top, sahadaki herhangi bir oyuncuya temas etmeden saha dışına çıkar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1, topu oyuna sokma ihlali yapmıştır. Oyun, orijinal topu oyuna sokma yerinden, B takımı tarafından topun oyuna sokulmasıyla devam edecektir. Şut saatinde: (a) Geri sahadan, 24 saniyeyle, (b) Ön sahadan, 14 saniyeyle.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-33\nAçıklama: Topu oyuna sokan oyuncu, topun oyuna sokulması sırasında top elinden çıktıktan sonra, topun saha dışına temas etmesine neden olmayacaktır.\nÖrnek 17-35: Topu oyuna sokan A1, A2’ye pas atar. A2, bir ayağı sınır çizgisine temas halindeyken topu yakalar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A2, topu oyuna sokma ihlali yapmıştır. Oyun B takımı tarafından, A2’nin sınır çizgisine temas ettiği en yakın yerden topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-33\nAçıklama: Topu oyuna sokan oyuncu, topun oyuna sokulması sırasında top elinden çıktıktan sonra, topun saha dışına temas etmesine neden olmayacaktır.\nÖrnek 17-36: A1’e kenar çizgiden topu oyuna sokma hakkı verilir: (a) Orta çizgiye yakın olan geri sahasından, topu sahadaki herhangi bir yere pas atma hakkıyla. (b) Orta çizgiye yakın ön sahasından, topu sadece ön sahasındaki bir takım arkadaşına pas atma hakkıyla. (c) Bir çeyreğin başında ya da her uzatmada or...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Tüm durumlarda, A1'in bu hareketi kurallara uygundur. A1, başlangıç durumuna göre topu ön sahasına veya geri sahasına pas verme hakkıyla birlikte ilk oyuna sokma pozisyonunu korur.",
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-37\nAçıklama: Sahadan yapılan başarılı bir sayı ya da son serbest atış sonrasında topu oyuna sokan oyuncu yana doğru ve/veya geriye doğru hareket edebilir ve dip çizginin gerisinde takım arkadaşıyla paslaşabilir ancak, topun oyuna sokulma süresi 5 saniyeyi geçemez. Bu aynı zamanda takımlardan herhangi biri tarafından bir mola alındıktan sonra veya savunma takımına top oyuna sokulurken bir ihlal çalındığında ve bu nedenle topun oyuna sokulması tekrarlandığında d...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Oyunu geciktirdiği için B2'e bir uyarı verilecektir. B2’in uyarısı ayrıca B takımının başantrenörüne iletilecek ve oyunun geri kalanındaki benzer durumlar için tüm B takımı üyelerine uygulanacaktır. Benzer bir hareketin tekrarı teknik faulle sonuçlanabilir. Herhangi bir A takımı oyuncusunun topu elinden çıkarmadan ya da takım arkadaşına pas vermeden önce dip çizgi boyunca hareket etme hakkı hala devam edecektir.",
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-37\nAçıklama: Sahadan yapılan başarılı bir sayı ya da son serbest atış sonrasında topu oyuna sokan oyuncu yana doğru ve/veya geriye doğru hareket edebilir ve dip çizginin gerisinde takım arkadaşıyla paslaşabilir ancak, topun oyuna sokulma süresi 5 saniyeyi geçemez. Bu aynı zamanda takımlardan herhangi biri tarafından bir mola alındıktan sonra veya savunma takımına top oyuna sokulurken bir ihlal çalındığında ve bu nedenle topun oyuna sokulması tekrarlandığında d...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu, B2 tarafından yapılan bir ayakla oynama ihlalidir. Oyun doğrudan arkalığın arkası hariç A takımı tarafından dip çizgisinden topun oyuna sokulmasıyla devam edecektir. B2’nin ayakla oynama ihlali topun oyuna sokulmasından sonra meydana geldiğinden, topu oyuna sokacak olan A takımı oyuncusunun topu oyuna sokarken dip çizgi boyunca hareket etme hakkı olmayacaktır.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-37\nAçıklama: Sahadan yapılan başarılı bir sayı ya da son serbest atış sonrasında topu oyuna sokan oyuncu yana doğru ve/veya geriye doğru hareket edebilir ve dip çizginin gerisinde takım arkadaşıyla paslaşabilir ancak, topun oyuna sokulma süresi 5 saniyeyi geçemez. Bu aynı zamanda takımlardan herhangi biri tarafından bir mola alındıktan sonra veya savunma takımına top oyuna sokulurken bir ihlal çalındığında ve bu nedenle topun oyuna sokulması tekrarlandığında d...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a), (b), (c) Bu, A takımının kurallara uygun oyunudur. (d) ve (e) Bu, A2 tarafından yapılan bir topu oyuna sokma ihlalidir.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-41\nAçıklama: Teknik faulün sonucunda kullanılan serbest atıştan sonra oyun, bir hava atışı durumu ya da birinci çeyreğin başı olmadıkça, teknik faul çalındığında topun olduğu en yakın yerden oyuna sokulmasıyla devam edecektir. Teknik faul savunma takımına verilirse, topun oyuna sokulması geri sahadan yönetiliyorsa hücum takımın şut saatinde 24 saniyesi olacaktır. Topun oyuna sokulması ön sahadan yönetiliyorsa, şut saati aşağıdaki gibi ayarlanacaktır: • Şut saa...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Her iki durumda da oyun, teknik faul meydana geldiğinde topun bulunduğu en yakın yerden, şut saatinde kalan süre ile A takımının topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-41\nAçıklama: Teknik faulün sonucunda kullanılan serbest atıştan sonra oyun, bir hava atışı durumu ya da birinci çeyreğin başı olmadıkça, teknik faul çalındığında topun olduğu en yakın yerden oyuna sokulmasıyla devam edecektir. Teknik faul savunma takımına verilirse, topun oyuna sokulması geri sahadan yönetiliyorsa hücum takımın şut saatinde 24 saniyesi olacaktır. Topun oyuna sokulması ön sahadan yönetiliyorsa, şut saati aşağıdaki gibi ayarlanacaktır: • Şut saa...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun, teknik faul meydana geldiğinde topun bulunduğu en yakın yerden A takımının topu oyuna sokmasıyla devam edecektir. Eğer (a) geri sahadaysa, şut saatinde 24 saniye ile (b) ön sahadaysa, şut saatinde 14 saniye veya daha fazla gösteriliyorsa kalan süre ile, şut saatinde 13 saniye veya daha az gösteriliyorsa, 14 saniye ile devam edilecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-41\nAçıklama: Teknik faulün sonucunda kullanılan serbest atıştan sonra oyun, bir hava atışı durumu ya da birinci çeyreğin başı olmadıkça, teknik faul çalındığında topun olduğu en yakın yerden oyuna sokulmasıyla devam edecektir. Teknik faul savunma takımına verilirse, topun oyuna sokulması geri sahadan yönetiliyorsa hücum takımın şut saatinde 24 saniyesi olacaktır. Topun oyuna sokulması ön sahadan yönetiliyorsa, şut saati aşağıdaki gibi ayarlanacaktır: • Şut saa...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Moladan sonra, herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun, teknik faul meydana geldiğinde topun bulunduğu en yakın yerden A takımının topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde kalan süresi kadar zamanı olacaktır.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-45\nAçıklama: Oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde, hücum takımına bir teknik faul çalınırsa ve bu takıma bir mola verilirse, sonrasında topun oyuna sokulması geri sahasından yönetilecekse, hücum takımının şut saati kalan süreden kadar zamanı olacaktır. Topun oyuna sokulması, ön sahasındaki topu oyuna sokma çizgisinden yönetilecekse, şut saati aşağıdaki şekilde ayarlanacaktır: • Şut saati 14 saniye veya daha fazla gösteri...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'En geç moladan sonra, A takımı başantrenörü topun oyuna sokulma yerini başhakeme bildirecektir (frontcourt “ön saha” ya da backcourt “geri saha”). Moladan sonra herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun, A takımının başantrenörünün kararına göre A takımının topu oyuna sokmasıyla devam edecektir. A takımı başantrenörü, kendi ön sahasındaki topu oyuna sokma çizgisinden topun oyuna sokulmasına karar verirse, eğer şut saati 14 saniye ya da daha fazla süre gösteriyorsa A takımının 14 saniyesi, eğer 13 saniye veya daha az gösteriyorsa, şut saatinde kalan süre kadar zamanı olacaktır. A takımı başantrenörü geri sahasından topun oyuna sokulmasına karar verirse A takımının şut saatinde kalan süresi kadar zamanı olacaktır.',
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-45\nAçıklama: Oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde, hücum takımına bir teknik faul çalınırsa ve bu takıma bir mola verilirse, sonrasında topun oyuna sokulması geri sahasından yönetilecekse, hücum takımının şut saati kalan süreden kadar zamanı olacaktır. Topun oyuna sokulması, ön sahasındaki topu oyuna sokma çizgisinden yönetilecekse, şut saati aşağıdaki şekilde ayarlanacaktır: • Şut saati 14 saniye veya daha fazla gösteri...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'En geç moladan sonra, A takımı başantrenörü topun oyuna sokulma yerini başhakeme bildirecektir (frontcourt “ön saha” ya da backcourt “geri saha”). Oyun, A takımının başantrenörünün kararına göre A takımının topu oyuna sokmasıyla devam edecektir. A takımı başantrenörü, kendi ön sahasındaki topu oyuna sokma çizgisinden topun oyuna sokulmasına karar verirse, eğer şut saati 14 saniye ya da daha fazla süre gösteriyorsa A takımının 14 saniyesi, eğer 13 saniye veya daha az gösteriyorsa, şut saatinde kalan süre kadar zamanı olacaktır. A takımı başantrenörü geri sahasından topun oyuna sokulmasına karar verirse A takımının şut saatinde kalan süresi kadar zamanı olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-45\nAçıklama: Oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde, hücum takımına bir teknik faul çalınırsa ve bu takıma bir mola verilirse, sonrasında topun oyuna sokulması geri sahasından yönetilecekse, hücum takımının şut saati kalan süreden kadar zamanı olacaktır. Topun oyuna sokulması, ön sahasındaki topu oyuna sokma çizgisinden yönetilecekse, şut saati aşağıdaki şekilde ayarlanacaktır: • Şut saati 14 saniye veya daha fazla gösteri...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'En geç moladan sonra, A takımı başantrenörü topun oyuna sokulma yerini başhakeme bildirecektir (frontcourt “ön saha” ya da backcourt “geri saha”). Moladan sonra herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun, A takımının başantrenörünün kararına göre A takımının topu oyuna sokmasıyla devam edecektir. A takımı başantrenörü, kendi ön sahasındaki topu oyuna sokma çizgisinden topun oyuna sokulmasına karar verirse, eğer şut saati 14 saniye ya da daha fazla süre gösteriyorsa A takımının 14 saniyesi, eğer 13 saniye veya daha az gösteriyorsa, şut saatinde kalan süre kadar zamanı olacaktır. A takımı başantrenörü geri sahasından topun oyuna sokulmasına karar verirse A takımının şut saatinde kalan süresi kadar zamanı olacaktır.',
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-45\nAçıklama: Oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde, hücum takımına bir teknik faul çalınırsa ve bu takıma bir mola verilirse, sonrasında topun oyuna sokulması geri sahasından yönetilecekse, hücum takımının şut saati kalan süreden kadar zamanı olacaktır. Topun oyuna sokulması, ön sahasındaki topu oyuna sokma çizgisinden yönetilecekse, şut saati aşağıdaki şekilde ayarlanacaktır: • Şut saati 14 saniye veya daha fazla gösteri...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A takımı başantrenörü oyunun, ön sahasındaki topu oyuna sokma çizgisinden mi yoksa geri sahasından mı topun oyuna sokularak devam edileceğine karar verecektir. Eğer topu, kendi ön sahasındaki topu oyuna sokma çizgisinden sokmaya karar verir ise, her durumda A takımının şut saatinde 14 saniyesi olacaktır. (a) ve (b) eğer geri sahasından sokmaya karar verirse, A takımının şut saatinde 24 saniyesi olacaktır. (c) eğer geri sahasından sokmaya karar verirse, A takımının şut saatinde 19 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-50\nAçıklama: Top sepete girdiğinde, ancak sahadan yapılan sayı ya da son serbest atış geçerli olmadığında oyun, serbest atış çizgisi uzantısından topun oyuna sokulmasıyla devam edecektir.\nÖrnek 17-51: A1, atış halindeyken yürüme ihlali yapar ve ardından top sepete girer.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in sayısı geçerli sayılmaz. B takımına geri sahasındaki serbest atış çizgisi uzantısından topu oyuna sokma hakkı verilecektir. B takımının şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 17 Topun oyuna sokulması | 17-50\nAçıklama: Top sepete girdiğinde, ancak sahadan yapılan sayı ya da son serbest atış geçerli olmadığında oyun, serbest atış çizgisi uzantısından topun oyuna sokulmasıyla devam edecektir.\nÖrnek 17-52: A1 sayı amacıyla sahadan bir şut atar. Top aşağı doğru iniş halindeyken A2 topa temas eder ve daha sonra top sepete girer.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in sayısı geçerli sayılmaz. B takımına geri sahasındaki serbest atış çizgisi uzantısından topu oyuna sokma hakkı verilecektir. B takımının şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-2: Top, oyunun başlangıcında hava atışında...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun başlamış olmasına rağmen oyun saati henüz çalışmadığından, mola ya da oyuncu değişikliği verilmeyecektir. 18/19- 3 Açıklama: Sayı amacıyla sahadan yapılan bir atış sırasında top havadayken şut saati sesli işaret verirse bu bir ihlal değildir ve oyun saati durmaz. Atılan şut başarılı olursa belirli koşullar altında, her iki takım için de bu bir mola ve oyuncu değişikliği fırsatıdır.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-4: Şut saati sesli işaretini verdiğinde, s...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Bu durum sadece, sayı yiyen takım için bir mola fırsatıdır. Sayı yiyen takıma bir mola verilirse rakiplerine de bir mola verilebilir ve eğer isterlerse her iki takıma da oyuncu değişikliği fırsatı verilebilir. (b) Bu durum sadece, dördüncü çeyrekte ve her uzatmada oyun saati 2:00 dakika ya da daha az gösterdiğinde sadece sayı yiyen takım için bir oyuncu değişikliği fırsatıdır. Sayı yiyen takıma oyuncu değişikliği hakkı verilirse rakiplerine de oyuncu değişikliği fırsatı verilebilir ve eğer isterlerse her iki takıma da mola verilebilir. 18/19- 5 Açıklama: Madde 18 ve 19, bir mola veya oyuncu değişikliği fırsatının ne zaman başlayıp bittiğini açıklar. Mola ya da oyuncu değişikliği talebi (serbest atışı atan oyuncu dahil, herhangi bir oyuncu için) top, ilk serbest atış için serbest atışı atacak oyuncunun kullanımında olduktan sonra istenirse, mola ya da oyuncu değişikliği aşağıdaki durumlarda her iki takım için de verilecektir, Eğer; (a) Son serbest atış başarılı olursa, veya (b) Son serbest atış sonrasını topun oyuna sokulması takip ediyorsa, veya (c) Son serbest atıştan sonra herhangi bir geçerli sebepten dolayı top ölü kalacaksa. Top, aynı faulün cezası için arka arkaya 2 veya 3 serbest atışın ilki için atışı kullanacak olan oyuncunun kullanımında olduktan sonra, son serbest atış sonrası top ölmeden önce herhangi bir mola veya oyuncu değişikliği verilmez. Bu tür serbest atışlar arasında bir teknik faul meydana geldiğinde, kimse dizilmeden serbest atış hemen yönetilecektir. Bir yedek oyuncu, teknik faul cezası için serbest atış yapacak oyuncu olmadıkça, her iki takıma da serbest atıştan önce ve / veya sonra bir mola veya oyuncu değişikliği verilmeyecektir. Bu durumda, rakipler de isterlerse 1 oyuncuyu değiştirme hakkına sahiptir.',
                'choices': [
                    ('Mola verilir', True),
                    ('Mola verilmez', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-6: A1’e 2 serbest atış hakkı verilir. Herh...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) İlk serbest atış girişiminden hemen önce, mola ya da oyuncu değişikliği verilecektir. (b) Başarılı olsa bile, ilk serbest atıştan sonra mola ya da oyuncu değişikliği verilmeyecektir. (c) Topun oyuna sokulmasından hemen önce, mola ya da oyuncu değişikliği verilecektir. (d) Mola ya da oyuncu değişikliği verilmeyecektir.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-7: A1’e 2 serbest atış hakkı verilir. İlk ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Mola ya da oyuncu değişikliği verilmeyecektir. (b), (c) ve (d) Mola ya da oyuncu değişikliği hemen verilecektir. (e) Yeni bir serbest atış A1 tarafından tekrar edilir ve eğer atış başarılı olursa, mola ya da oyuncu değişikliği hemen verilecektir.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-8: Bir oyuncu değişikliği fırsatı henüz bi...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Hakemin oyunu durdurmasından dolayı normal olarak bir değişiklik fırsatıyla sonuçlanacak şekilde top ölüdür ve oyun saati durmuştur. Ancak, A6’nın isteği çok geç yapıldığı için oyuncu değişikliği yapılmayacaktır. Oyun hemen devam ettirilecektir.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-9: Oyun sırasında sayıya yönelen top veya ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'İhlal, oyun saatinin durmasına ve topun ölmesine neden olur. Mola veya oyuncu değişikliği verilecektir.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-10: B1, başarısız 2 sayılık atış girişimin...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. B takımının bir yedek oyuncusu, serbest atış atacak bir oyuncu haline gelirse, A takımı da isterse 1 oyuncuyu değiştirme hakkına sahiptir. Serbest atış, oyuncu olmuş bir B takımının yedek oyuncusu tarafından kullanılırsa veya A takımı da 1 oyuncu değiştirdiyse, bir sonraki oyun saatinin çalışma periyodu bitene kadar bu oyuncular değiştirilemez. B takımı oyuncusunun, A2'ye verilen teknik faul için kullandığı serbest atışından sonra A1 ikinci serbest atışını kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir. Eğer son serbest atış başarılı olursa ve talep edilirse her iki takıma da mola veya oyuncu değişikliği verilecektir.",
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-11: B1, başarısız 2 sayılık atış girişimin...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu sırada mola veya oyuncu değişikliği yapılmayacaktır. A1, ikinci serbest atışını kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir. Eğer son serbest atış başarılı olursa ve talep edilirse her iki takıma da mola veya oyuncu değişikliği verilecektir.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-12: B1, başarısız 2 sayılık atış girişimin...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A2, hemen değiştirilecektir. Herhangi bir B takımı oyuncusu, kimse dizilmeden 1 serbest atış atabilir. B takımının bir yedek oyuncusu, serbest atış atacak bir oyuncu haline gelirse, A takımı da isterse 1 oyuncuyu değiştirme hakkına sahip olacaktır. Serbest atış, oyuncu olmuş bir B takımının yedek oyuncusu tarafından kullanılırsa veya A takımı da 1 oyuncuyu değiştirdiyse, bir sonraki oyun saatinin çalışma periyodu bitene kadar bu oyuncular değiştirilemez. B takımı oyuncusunun, A2'ye verilen teknik faul için kullandığı serbest atışından sonra A1, ikinci serbest atışını kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir. Eğer son serbest atış başarılı olursa ve talep edilirse her iki takıma da mola veya daha fazla oyuncu değişikliği verilecektir.",
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': "Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-13: Dripling yapmakta olan A1'e bir teknik...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Bu, iki takım için de bir oyuncu değişikliği fırsatıdır. B6 bir oyuncu olduktan sonra, kimse dizilmeden 1 serbest atış atabilir ancak, bir sonraki oyun saatinin çalışma periyodu bitene kadar değişemeyecektir. 18/19- 14 Açıklama: Oyuncu değişikliği sonucunda sahada oyuncu olan bir yedek oyuncu, ancak oyunun bir sonraki oyun saati çalışma periyodunun bitiminden sonra oyundan çıkabilir/değişebilir.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-15: B1, B6 ile değiştirilir. Oyun saati ba...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) B6, bir sonraki oyun saatinin çalışma periyodu bitene kadar değişemeyecektir. (b) B6 değiştirilecektir. 18/19- 16 Açıklama: Bir mola isteği sonrasında herhangi bir takım tarafından faul yapılırsa, hakemin bu faulle ilgili hakem masasıyla tüm iletişimi tamamlanıncaya kadar mola başlamayacaktır. Bir oyuncunun beşinci faulü olması durumunda bu iletişim, gerekli oyuncu değişikliği prosedürünü de içerir. Tüm iletişim tamamlandıktan sonra mola periyodu, bir hakemin düdüğünü çalması ve mola işaretini göstermesiyle başlayacaktır.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-17: Oyun sırasında A takımı başantrenörü b...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "(a) Mola periyodu, hakem masasıyla bu faulle ilgili tüm iletişimin tamamlanması ve B1'le değişecek bir yedek oyuncunun, sahada oyuncu olmasına kadar başlamayacaktır. Her iki durumda da, mola süresi resmi olarak başlamamış olsa bile oyuncuların takım sıra bölgelerine gitmelerine izin verilecektir. 18/19- 18 Açıklama: Her mola 1 dakika sürecektir. Hakem düdüğünü çaldıktan ve takımları sahaya çağırdıktan sonra takımlar hemen sahaya dönmelidir. Bir takım mola süresini 1 dakikadan daha fazla uzatırsa, molayı süresini uzatarak bir avantaj elde etmektedir ve ayrıca oyunun gecikmesine neden olmaktadır. Bu takımın başantrenörüne hakem tarafından bir uyarı verilecektir. Başantrenör uyarıya duyarsız kalırsa bu takıma ek bir mola verilecektir. Bu takımın molası kalmamışsa oyunu geciktirdikleri için başantrenöre maç kağıdına ‘B1 ’ kaydedilen bir teknik faul verilebilir. Eğer bir takım, oyunun devre arasından sonra hemen sahaya dönmezse bu takıma bir mola verilecektir. Bu şekilde verilen mola 1 dakika sürmeyecektir. Oyun hemen devam ettirilecektir.",
                'choices': [
                    ('İzin verilir', True),
                    ('izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-19: Mola biter ve hakem A takımını sahaya ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) A takımı sahaya dönmeye başladıktan sonra hakem, A takımı başantrenörüne aynı davranışın tekrarlanması durumunda A takımına ek bir mola verileceği yönünde bir uyarı verecektir. (b) A takımına uyarı yapılmadan bir mola verilecektir. Bu mola 1 dakika sürecektir. A takımının molası kalmamışsa, oyunu geciktirdikleri için A takımı başantrenörüne ‘B1 ’ kaydedilen bir teknik faul verilecektir. 18/19–20 Örnek: Devre arasındaki oyun arasından sonra A takımı hala soyunma odasındadır ve bu nedenle üçüncü çeyreğin başlaması gecikmektedir. A takımı nihayetinde sahaya geldikten sonra, uyarı yapılmadan A takımına bir mola verilecektir. Bu mola 1 dakika sürmeyecektir. Oyun hemen devam ettirilecektir. 18/19- 21 Açıklama: Bir takım ikinci devrede, oyun saati dördüncü çeyrekte 2:00 gösterene kadar bir mola almamışsa sayı görevlisi maç kağıdındaki takımın ikinci devre molaları için olan birinci kutuya 2 yatay çizgi çizecektir. Skorbord, birinci mola alınmış gibi gösterecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-22: Dördüncü çeyrekte oyun saatinde 2:00 k...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Sayı görevlisi, maç kağıdında ikinci devre için her iki takımın molalarının ilk kutusunu 2 yatay çizgi ile işaretleyecektir. Skorbord, birinci mola alınmış gibi gösterecektir.',
                'choices': [
                    ('Sayı görevlisi, maç kağıdında ikinci devre için her iki takımın molalarının ilk kutusunu 2 yatay çizgi ile işaretleyecektir. Skorbord, birinci mola alınmış gib…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-23: Dördüncü çeyrekte oyun saatinde 2:09 k...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Mola, oyun saati dördüncü çeyrekte 2:00 göstermeden önce verilmediğinden, sayı görevlisi maç kağıdında A takımının molalarının ilk kutusunu 2 yatay çizgi ile işaretleyecektir. Mola 1:58’de verildiğinden ikinci kutuya kaydedilecek ve A takımının sadece 1 molası kalacaktır. Moladan sonra skorbord, 2 mola alınmış gibi gösterecektir. 18/19- 24 Açıklama: Bir mola istendiğinde bir teknik, sportmenlik dışı ya da diskalifiye edici faul çalınmasından önce ya da sonra olduğuna bakılmaksınız mola, serbest atış ya da atışların yönetimi başlamadan önce verilmelidir. Bir mola sırasında bir teknik, sportmenlik dışı veya diskalifiye edici faul verilirse, serbest atış ya da atışlar mola tamamlandıktan sonra yönetilecektir.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-25: B takımı başantrenörü bir mola ister. ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B takımına bir mola verilecektir. Moladan sonra, herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Daha sonra B1, kimse dizilmeden 2 serbest atış kullanacaktır. Oyun, B takımının ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 18/19 Mola / Oyuncu değişikliği | 18/19-1\nAçıklama: Bir çeyrek ya da uzatma için oyun süresinin başlamasından önce veya bir çeyrek ya da uzatma için oyun süresinin bitmesinden sonra bir mola verilemez. Birinci çeyrek için oyun süresinin başlamasından önce ya da maç için oyun süresinin bitmesinden sonra bir oyuncu değişikliği yapılamaz. Çeyrekler ve uzatmalar arasındaki oyun araları sırasında herhangi bir oyuncu değişikliği yapılabilir.\nÖrnek 18/19-26: B takımı başantrenörü bir mola ister. ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Moladan sonra, herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Daha sonra B1, kimse dizilmeden 2 serbest atış kullanacaktır. Oyun, B takımının ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 23 Saha dışı oyuncu ve saha dışı top | 23-1\nAçıklama: Top, sınır çizgisi üzerinde veya dışında bulunan bir oyuncunun dokunması veya topa temas etmesi nedeniyle saha dışına giderse, bu oyuncu topun saha dışına çıkmasına neden olur.\nÖrnek 23-2: Kenar çizgiye yakın top ellerinde olan A1, B1 tarafından yakından savunulmaktadır. A1, bir ayağı saha dışında olan B1’e vücudu ile temas eder.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A1'in bu hareketi kurallara uygundur Bir oyuncu, vücudunun herhangi bir kısmı bir oyuncudan başka bir şeyle temas ettiğinde saha dışındadır. Oyun devam edecektir.",
                'choices': [
                    ("A1'in bu hareketi kurallara uygundur Bir oyuncu, vücudunun herhangi bir kısmı bir oyuncudan başka bir şeyle temas ettiğinde saha dışındadır. Oyun devam edecekt…", True),
                    ("A1'in bu hareketi kurallara uygun değildir Bir oyuncu, vücudunun herhangi bir kısmı bir oyuncudan başka bir şeyle temas ettiğinde saha dışındadır. Oyun devam edecekt…", False),
                ]
            },
            {
                'text': "Madde 23 Saha dışı oyuncu ve saha dışı top | 23-1\nAçıklama: Top, sınır çizgisi üzerinde veya dışında bulunan bir oyuncunun dokunması veya topa temas etmesi nedeniyle saha dışına giderse, bu oyuncu topun saha dışına çıkmasına neden olur.\nÖrnek 23-3: Kenar çizgiye yakın, top ellerinde olan A1, B1 ve B2 tarafından yakından savunulmaktadır. A1, bir ayağı saha dışında olan B1'e topla temas eder.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Bu, B1 tarafından yapılan bir saha dışı ihlalidir. Top, saha dışındaki bir oyuncuya temas ettiğinde saha dışına çıkmıştır. Oyun, A takımı tarafından doğrudan arkalığın arkası hariç, topun saha dışına çıktığı en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde kalan süre kadar zamanı olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': "Madde 23 Saha dışı oyuncu ve saha dışı top | 23-1\nAçıklama: Top, sınır çizgisi üzerinde veya dışında bulunan bir oyuncunun dokunması veya topa temas etmesi nedeniyle saha dışına giderse, bu oyuncu topun saha dışına çıkmasına neden olur.\nÖrnek 23-4: A1, hakem masasının önünde kenar çizgisine yakın dripling yapmaktadır. Top, sahadan sekerek oyuncu değişikliği sandalyesinde oturan B6'nın dizine temas eder ve sonrasında tekrardan sahadaki A1'e geri gelir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Top, saha dışı olan B6'ya temas ettiğinde saha dışına çıkmıştır. Topun saha dışına çıkmasına, saha dışına çıkmadan önce topa son dokunan A1 neden olmuştur. Oyun B takımı tarafından, doğrudan arkalığın arkası hariç, topun saha dışına çıktığı en yakın yerden topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 24 Dripling | 24-1\nAçıklama: Bir oyuncunun kasıtlı olarak topu rakibinin ya da kendi arkalığına atması dripling değildir.\nÖrnek 24-2: A1 henüz dripling yapmamıştır ve kasıtlı olarak topu arkalığa doğru attığında ve başka bir oyuncuya dokunmadan önce topu tekrar yakaladığında veya temas ettiğinde hareketsiz durmaktadır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in hareketi kurallara uygundur. A1 topu yakaladıktan sonra şut atabilir, pas verebilir ya da driplinge başlayabilir.',
                'choices': [
                    ('A1’in hareketi kurallara uygundur. A1 topu yakaladıktan sonra şut atabilir, pas verebilir ya da driplinge başlayabilir.', True),
                    ('A1’in hareketi kurallara uygun değildir. A1 topu yakaladıktan sonra şut atabilir, pas verebilir ya da driplinge başlayabilir.', False),
                ]
            },
            {
                'text': 'Madde 24 Dripling | 24-1\nAçıklama: Bir oyuncunun kasıtlı olarak topu rakibinin ya da kendi arkalığına atması dripling değildir.\nÖrnek 24-3: A1, devam eden hareketindeyken ya da hareketsiz dururken driplingini tamamlandıktan sonra kasıtlı olarak topu arkalığına doğru atar. A1 aşağıdaki durumlarda topu tekrar yakalar veya topa temas eder. (a) Top sahada seker ve driplinge başlar. (b) Başka bir oyuncuya temas etmeden önce.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "(a) Bu A1’in yaptığı çift dripling ihlalidir. A1, ilk driplingi bitirdikten sonra ikinci kez dripling yapamayacaktır. (b) A1’in hareketi kurallara uygundur. A1 topu yakaladıktan sonra şut atabilir, pas verebilir ancak yeni bir driplinge başlayamaz. İlk driplingi bitirdikten sonra ikinci kez dripling yapmayacağı için bu A1'in çift dripling ihlalidir.",
                'choices': [
                    ('Çift dripling ihlali', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 24 Dripling | 24-1\nAçıklama: Bir oyuncunun kasıtlı olarak topu rakibinin ya da kendi arkalığına atması dripling değildir.\nÖrnek 24-4: A1’in sahadan attığı şut çembere temas etmez. A1 topu yakalar ve kasıtlı olarak arkalığa doğru atar, sonrasında başka bir oyuncuya dokunmadan önce topu tekrar yakalar veya topa temas eder.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in hareketi kurallara uygundur. A1 topu yakaladıktan sonra şut atabilir, pas verebilir ya da driplinge başlayabilir.',
                'choices': [
                    ('A1’in hareketi kurallara uygundur. A1 topu yakaladıktan sonra şut atabilir, pas verebilir ya da driplinge başlayabilir.', True),
                    ('A1’in hareketi kurallara uygun değildir. A1 topu yakaladıktan sonra şut atabilir, pas verebilir ya da driplinge başlayabilir.', False),
                ]
            },
            {
                'text': 'Madde 24 Dripling | 24-1\nAçıklama: Bir oyuncunun kasıtlı olarak topu rakibinin ya da kendi arkalığına atması dripling değildir.\nÖrnek 24-5: A1 dripling yapar ve kurallara uygun olarak durur. Devamında: (a) A1 daha sonra dengesini kaybeder ve topu el ya da ellerinde tutarken pivot ayağını hareket ettirmeden bir veya iki kez topla zemine temas eder. (b) A1 daha sonra pivot ayağını hareket ettirmeden topu bir elinden diğerine atar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da A1’in bu hareketi kurallara uygundur. A1, pivot ayağını hareket ettirmemiştir.',
                'choices': [
                    ('Her iki durumda da A1’in bu hareketi kurallara uygundur. A1, pivot ayağını hareket ettirmemiştir.', True),
                    ('Her iki durumda da A1’in bu hareketi kurallara uygun değildir. A1, pivot ayağını hareket ettirmemiştir.', False),
                ]
            },
            {
                'text': 'Madde 24 Dripling | 24-1\nAçıklama: Bir oyuncunun kasıtlı olarak topu rakibinin ya da kendi arkalığına atması dripling değildir.\nÖrnek 24-6: A1, aşağıdaki durumlarda driplinge başlar: (a) Topu rakibinin üzerinden atarak. (b) Topu kendisinden birkaç metre uzağa atarak. Top oyun sahasına temas eder ve ardından A1 driplingine devam eder.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da A1’in bu hareketi kurallara uygundur. A1, driplinginde topa tekrar temas etmeden önce top oyun sahasına temas etmiştir.',
                'choices': [
                    ('Her iki durumda da A1’in bu hareketi kurallara uygundur. A1, driplinginde topa tekrar temas etmeden önce top oyun sahasına temas etmiştir.', True),
                    ('Her iki durumda da A1’in bu hareketi kurallara uygun değildir. A1, driplinginde topa tekrar temas etmeden önce top oyun sahasına temas etmiştir.', False),
                ]
            },
            {
                'text': "Madde 24 Dripling | 24-1\nAçıklama: Bir oyuncunun kasıtlı olarak topu rakibinin ya da kendi arkalığına atması dripling değildir.\nÖrnek 24-7: A1, driplingini bitirir ve kasıtlı olarak topu B1'in bacağına atar. A1 topu yakalar ve tekrar driplinge başlar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Bu A1'in çift dripling ihlalidir. Topa B1 tarafından temas edilmediği için A1'in driplingi sona ermiştir. B1’e temas eden toptu. A1 tekrar dripling yapamaz.",
                'choices': [
                    ('Çift dripling ihlali', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "Madde 25 Yürüme | 25-1\nAçıklama: Sahada uzanarak yatan bir oyuncu topun kontrolünü kazanırsa kurallara uygundur. Topu tutan bir oyuncu sahaya düşerse bu da kurallara uygundur. Bir oyuncu topla zemine düştükten sonra biraz kayarsa bu durum da kurallara uygundur. Ancak oyuncu, topu tutarken yuvarlanır ya da ayağa kalkma girişiminde bulunursa bu bir ihlaldir.\nÖrnek 25-2: A1’in top ellerindeyken; (a) dengesini kaybeder ve sahaya düşer. (b) sahaya düştükten sonra A1'in düşme hızı o oyuncunun zeminde ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Her iki durumda da A1’in bu hareketi kurallara uygundur. Sahaya düşmesi bir yürüme ihlali değildir. Ancak A1, savunmadan kaçmak için top ellerindeyken yuvarlanır ya da ayağa kalkma girişiminde bulunursa bu bir yürüme ihlali olur.',
                'choices': [
                    ('Yürüme ihlali (top kaybı)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 25 Yürüme | 25-1\nAçıklama: Sahada uzanarak yatan bir oyuncu topun kontrolünü kazanırsa kurallara uygundur. Topu tutan bir oyuncu sahaya düşerse bu da kurallara uygundur. Bir oyuncu topla zemine düştükten sonra biraz kayarsa bu durum da kurallara uygundur. Ancak oyuncu, topu tutarken yuvarlanır ya da ayağa kalkma girişiminde bulunursa bu bir ihlaldir.\nÖrnek 25-3: A1, sahada zemininde uzanarak yatarken topun kontrolünü kazanır. A1, daha sonra: (a) Topu A2’ye pas atar. (b) Sahada uzanarak yat...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a), (b) ve (c) A1’in bu hareketi kurallara uygundur. (d) A1 tarafından yapılmış bir yürüme ihlalidir.',
                'choices': [
                    ('Yürüme ihlali (top kaybı)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 25 Yürüme | 25-4\nAçıklama: Bir oyuncu driplingini bitirdikten ya da topun kontrolünü kazandıktan sonra aynı ayağıyla veya her iki ayağıyla arka arkaya sahaya temas edemez.\nÖrnek 25-5: A1, top ellerindeyken driplingini bitirir. Devam eden hareketinde A1 sol ayağı ile sıçrar, sol ayağı ile sahaya temas eder, sonra sağ ayağına iner ve sayı amacıyla şut atma girişiminde bulunur.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu, A1 tarafından yapılmış bir yürüme ihlalidir. Bir oyuncu driplingini bitirdikten sonra aynı ayağıyla arka arakaya sahaya temas edemez.',
                'choices': [
                    ('Yürüme ihlali (top kaybı)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 25 3 saniye | 26-1\nAçıklama: Bir oyuncunun, 3 saniye ihlalinden kaçınmak için dip çizgiden oyun sahasını terk etmesi ve ardından kısıtlamalı alana tekrar girmesi bir ihlaldir.\nÖrnek 26-2: Kısıtlamalı alanda 3 saniyeden daha az kalan A1, 3 saniye ihlalinden kaçınmak için dip çizgiden sahanın dışına çıkar ve daha sonra kısıtlamalı alana tekrar girer.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1, 3 saniye ihlali yapmıştır.',
                'choices': [
                    ('A1, 3 saniye ihlali yapmıştır.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 25 3 saniye | 26-3\nAçıklama: Kendi takımı ön sahada canlı bir topu kontrol ederken ve oyun saati çalışırken, bu takımın bir oyuncusu rakibinin kısıtlamalı alanında art arda 3 saniyeden fazla kalamaz.\nÖrnek 26-4: Topu sayı amacıyla elden çıkardığında A1 2.5 saniye boyunca kısıtlamalı alanda bulunmaktadır. Top arkalığa veya çembere temas etmez ve A1 ribaundu alır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A1’in bu hareketi kurallara uygundur. A1 sayı amacıyla topu elinden çıkardığında A takımının top kontrolünü sona ermiştir. A1'in ribaundu ile A takımı topun kontrolünü yeniden kazanmıştır.",
                'choices': [
                    ("A1’in bu hareketi kurallara uygundur. A1 sayı amacıyla topu elinden çıkardığında A takımının top kontrolünü sona ermiştir. A1'in ribaundu ile A takımı topun ko…", True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 25 3 saniye | 26-3\nAçıklama: Kendi takımı ön sahada canlı bir topu kontrol ederken ve oyun saati çalışırken, bu takımın bir oyuncusu rakibinin kısıtlamalı alanında art arda 3 saniyeden fazla kalamaz.\nÖrnek 26-5: Top ön sahada, topu oyuna sokacak olan A1’in ellerindeyken A2, 3 saniyeden fazla rakibin kısıtlamalı alanında bulunmaktadır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A2’in bu hareketi kurallara uygundur. A takımı topun kontrolüne sahiptir, ancak oyun saati henüz başlamamıştır.',
                'choices': [
                    ('A2’in bu hareketi kurallara uygundur. A takımı topun kontrolüne sahiptir, ancak oyun saati henüz başlamamıştır.', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 28 8 saniye | 28-1\nAçıklama: Şut saati bir hava atışı durumu nedeniyle durdurulur. Hava atışı durumu sonucunda pozisyon sırasına göre topun oyuna sokulması, kendi geri sahasında topu kontrol eden takıma verilirse 8 saniye süresi devam edecektir.\nÖrnek 28-2: Bir tutulmuş top durumu oluştuğunda A1, 5 saniye boyunca kendi geri sahasında dripling yapmıştır. A Takımı bir sonraki pozisyon sırasına göre topu oyuna sokma hakkına sahiptir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A takımının topu ön sahasına geçirmesi için sadece 3 saniyesi olacaktır.',
                'choices': [
                    ('A takımının topu ön sahasına geçirmesi için sadece 3 saniyesi olacaktır.', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 28 8 saniye | 28-3\nAçıklama: Geri sahadan ön sahaya yapılan dripling sırasında, dripling yapan oyuncunun her iki ayağı ve top tamamen ön sahayla temas halindeyken top, bir takımın ön sahasındadır.\nÖrnek 28-4: A1’in ayakları orta çizginin iki yanındadır ve geri sahasındaki A2’den bir pas alır. A1 daha sonra topu A2’ye pas olarak atar. A2; (a) hala geri sahasındadır. (b) ayakları orta çizginin iki yanındadır. (c) ayakları orta çizginin iki yanındadır. A2, kendi geri sahasında driplinge başla...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda bu A takımının kurallara uygun bir oyundur. A1’in her iki ayağı da tamamen ön sahaya temas etmemektedir ve bu nedenle A1’in, topu geri sahasına atma hakkı vardır. 8 saniye süresi devam edecektir.',
                'choices': [
                    ('Tüm durumlarda bu A takımının kurallara uygun bir oyundur. A1’in her iki ayağı da tamamen ön sahaya temas etmemektedir ve bu nedenle A1’in, topu geri sahasına …', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 28 8 saniye | 28-3\nAçıklama: Geri sahadan ön sahaya yapılan dripling sırasında, dripling yapan oyuncunun her iki ayağı ve top tamamen ön sahayla temas halindeyken top, bir takımın ön sahasındadır.\nÖrnek 28-5: A1 kendi geri sahasında dripling yapar ve hala dripling yapmaya devam ederken ileriye doğru gidiş hareketini durdurur. Bu sırada A1: (a) Ayakları, orta çizginin iki yanında durmaktadır. (b) Topla geri sahasında dripling yaparken, her iki ayağı da ön sahasındadır. (c) Topla geri sahası...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda bu, A1’in kurallara uygun bir hareketidir. Dripling yapan A1, hem her iki ayağı hem de top, tamamen ön sahadaki zemine temas edene kadar geri sahasında olmaya devam edebilir. 8 saniye süresi devam edecektir.',
                'choices': [
                    ('Tüm durumlarda bu, A1’in kurallara uygun bir hareketidir. Dripling yapan A1, hem her iki ayağı hem de top, tamamen ön sahadaki zemine temas edene kadar geri sa…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 28 8 saniye | 28-6\nAçıklama: 8 saniye periyodu, kalan süre ile devam ettiğinde ve daha önce topu kontrol eden aynı takıma geri sahasından topu oyuna sokma hakkı verildiğinde hakem topu, oyuna sokacak olan oyuncuya verirken, 8 saniye periyodunda kalan süreyi topu oyuna sokacak olan oyuncuya bildirecektir.\nÖrnek 28-7: A1, geri sahasında 6 saniye boyunca dripling yaptığında, bir çift faul verilir: (a) Geri sahada (b) Ön sahada.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Oyun, A takımı tarafından geri sahasında, çift faulün olduğu en yakın yerden topu oyuna sokmasıyla devam edecektir. Hakem, topu oyuna sokan A takımının topu oyuna sokacak olan oyuncusuna topu kendi ön sahasına götürebilmesi için 2 saniyesi olduğunu bildirecektir. (b) Oyun, A takımı tarafından ön sahasında, çift faulün olduğu en yakın yerden topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 28 8 saniye | 28-6\nAçıklama: 8 saniye periyodu, kalan süre ile devam ettiğinde ve daha önce topu kontrol eden aynı takıma geri sahasından topu oyuna sokma hakkı verildiğinde hakem topu, oyuna sokacak olan oyuncuya verirken, 8 saniye periyodunda kalan süreyi topu oyuna sokacak olan oyuncuya bildirecektir.\nÖrnek 28-8: B1 topu, A takımının geri sahasında saha dışına tiplediğinde A1, geri sahasında 4 saniye dripling yapmıştır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun A takımı tarafından kendi geri sahasında, topun saha dışına çıktığı en yakın yerden topu oyuna sokmasıyla devam edecektir. Hakem, A takımının topu oyuna sokacak olan oyuncusuna topu ön sahasına götürebilmesi için 4 saniyesi olduğunu bildirecektir.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 28 8 saniye | 28-9\nAçıklama: Oyun, bir hakem tarafından her iki takımı da ilgilendirmeyen herhangi bir geçerli nedenle durdurulursa ve hakemlerin değerlendirmesine göre rakipler dezavantajlı bir duruma düşerse, 8 saniye süresi devam edecektir.\nÖrnek 28-10: Dördüncü çeyrekte oyun saatinde 25 saniye kala ve skor A 72 – B 72 iken A takımı topun kontrolünü kazanır. Oyun, hakemler tarafından aşağıdaki nedenlerle durdurulduğunda A1 4 saniye boyunca kendi geri sahasında dripling yapmıştır: (a) Oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda oyun, A takımının kendi geri sahasından 8 saniye periyodunda 4 saniye süre kalacak şekilde topu oyuna sokmasıyla devam edecektir. Eğer oyun, yeni bir 8 saniye periyodu süresi ile devam ettirilirse, B takımı dezavantajlı duruma düşecektir.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 28 8 saniye | 28-11\nAçıklama: 8 saniye periyodu ihlalinden sonra topu oyuna sokma yeri, ihlalin meydana geldiği andaki yere göre belirlenir.\nÖrnek 28-12: A takımının 8 saniye periyodu aşağıdaki durumlarda sona erer ve ihlal meydana gelir. (a) A takımı topu, geri sahasında kontrol ederken. (b) Top, A1’in pasında, kendi geri sahasından ön sahasına doğru giderken havadadır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B takımının topu oyuna sokması, kendi ön sahasındaki; (a) Doğrudan arkalığın arkası hariç, 8 saniye ihlali meydana geldiğinde topun olduğu yerden. (b) Orta çizgiye en yakın yerden yapılacaktır. B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-1\nAçıklama: Şut saati periyodunun bitmesine yakın, sayı amacıyla sahadan bir şut atılır ve top havadayken şut saati sesli işaret verir. • Eğer top çemberden içeri geçerse sayı geçerli sayılacaktır. • Eğer top çembere temas etmezse hakemler, rakip takımın hemen ve açık bir şekilde topun kontrolünü sağlayıp sağlayamadığını görmek için bekleyecektir. — Eğer rakip takım topun kontrolünü sağlarsa şut saati sesli işareti dikkate alınmayacaktır. — Eğer rakip takım topun ko...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu, A takımı tarafından yapılan bir şut saati ihlalidir. A1’in sahadan attığı şutta top çembere temas etmemiştir ve B takımı hemen ve açık bir şekilde topun kontrolünü kazanamamıştır.',
                'choices': [
                    ('Şut saati ihlali', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-1\nAçıklama: Şut saati periyodunun bitmesine yakın, sayı amacıyla sahadan bir şut atılır ve top havadayken şut saati sesli işaret verir. • Eğer top çemberden içeri geçerse sayı geçerli sayılacaktır. • Eğer top çembere temas etmezse hakemler, rakip takımın hemen ve açık bir şekilde topun kontrolünü sağlayıp sağlayamadığını görmek için bekleyecektir. — Eğer rakip takım topun kontrolünü sağlarsa şut saati sesli işareti dikkate alınmayacaktır. — Eğer rakip takım topun ko...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu, A takımı tarafından yapılan bir şut saati ihlalidir.',
                'choices': [
                    ('Şut saati ihlali', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-1\nAçıklama: Şut saati periyodunun bitmesine yakın, sayı amacıyla sahadan bir şut atılır ve top havadayken şut saati sesli işaret verir. • Eğer top çemberden içeri geçerse sayı geçerli sayılacaktır. • Eğer top çembere temas etmezse hakemler, rakip takımın hemen ve açık bir şekilde topun kontrolünü sağlayıp sağlayamadığını görmek için bekleyecektir. — Eğer rakip takım topun kontrolünü sağlarsa şut saati sesli işareti dikkate alınmayacaktır. — Eğer rakip takım topun ko...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Bu, A takımı tarafından yapılan bir şut saati ihlalidir. B1'in A1’e karşı yaptığı faul, sportmenlik dışı ya da diskalifiye edici faul olmadıkça dikkate alınmayacaktır.",
                'choices': [
                    ('Şut saati ihlali', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-1\nAçıklama: Şut saati periyodunun bitmesine yakın, sayı amacıyla sahadan bir şut atılır ve top havadayken şut saati sesli işaret verir. • Eğer top çemberden içeri geçerse sayı geçerli sayılacaktır. • Eğer top çembere temas etmezse hakemler, rakip takımın hemen ve açık bir şekilde topun kontrolünü sağlayıp sağlayamadığını görmek için bekleyecektir. — Eğer rakip takım topun kontrolünü sağlarsa şut saati sesli işareti dikkate alınmayacaktır. — Eğer rakip takım topun ko...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da bu, A takımı tarafından yapılan bir şut saati ihlalidir. B takımı hemen ve açık bir şekilde topun kontrolünü kazanamamıştır.',
                'choices': [
                    ('Şut saati ihlali', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-1\nAçıklama: Şut saati periyodunun bitmesine yakın, sayı amacıyla sahadan bir şut atılır ve top havadayken şut saati sesli işaret verir. • Eğer top çemberden içeri geçerse sayı geçerli sayılacaktır. • Eğer top çembere temas etmezse hakemler, rakip takımın hemen ve açık bir şekilde topun kontrolünü sağlayıp sağlayamadığını görmek için bekleyecektir. — Eğer rakip takım topun kontrolünü sağlarsa şut saati sesli işareti dikkate alınmayacaktır. — Eğer rakip takım topun ko...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '',
                'choices': [
                    ('Şut saati ihlali', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-1\nAçıklama: Şut saati periyodunun bitmesine yakın, sayı amacıyla sahadan bir şut atılır ve top havadayken şut saati sesli işaret verir. • Eğer top çemberden içeri geçerse sayı geçerli sayılacaktır. • Eğer top çembere temas etmezse hakemler, rakip takımın hemen ve açık bir şekilde topun kontrolünü sağlayıp sağlayamadığını görmek için bekleyecektir. — Eğer rakip takım topun kontrolünü sağlarsa şut saati sesli işareti dikkate alınmayacaktır. — Eğer rakip takım topun ko...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Bu, A takımının bir şut saati ihlali değildir. Hakem, B takımının topun kontrolünü hemen ve açık bir şekilde kazanıp kazanmadığını görmek için beklerken ihlali çalmamıştır. Çeyrek sona ermiştir. (b) Bu, A takımının şut saati ihlalidir. Oyun, oyun saatinde 0.8 saniyeyle oyunun durdurulduğu en yakın yerden B takımının topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Şut saati ihlali: Top B takımına verilir', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-1\nAçıklama: Şut saati periyodunun bitmesine yakın, sayı amacıyla sahadan bir şut atılır ve top havadayken şut saati sesli işaret verir. • Eğer top çemberden içeri geçerse sayı geçerli sayılacaktır. • Eğer top çembere temas etmezse hakemler, rakip takımın hemen ve açık bir şekilde topun kontrolünü sağlayıp sağlayamadığını görmek için bekleyecektir. — Eğer rakip takım topun kontrolünü sağlarsa şut saati sesli işareti dikkate alınmayacaktır. — Eğer rakip takım topun ko...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu, A takımı tarafından yapılan bir şut saati ihlalidir. İhlal, oyun saatinde 1.2 saniye varken gerçekleştiğinden hakemler oyun saatini düzeltmeye karar verirler. Oyun, oyun saatinde 1.2 saniyeyle oyunun durdurulduğu en yakın yerden B takımının topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Şut saati ihlali: Top B takımına verilir', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-9\nAçıklama: Şut saati sesli işaret verirse ve hakemlerin değerlendirmesine göre rakipler, hemen ve açık bir şekilde topun kontrolünü kazanırsa, şut saati sesli işareti dikkate alınmayacaktır. Oyun devam edecektir.\nÖrnek 29/50-10: Şut saati periyodunun sonuna yakın, A1’in pası A2 tarafından alınamaz (her iki oyuncu da kendi ön sahalarındadır) ve top A takımının geri sahasına yuvarlanır. Sepete doğru serbest bir yolu olan B1, topun kontrolünü elde etmeden önce şut saa...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Eğer B1, hemen ve açık bir şekilde topun kontrolünü kazanırsa, sesli işaret dikkate alınmayacaktır. Oyun devam edecektir.',
                'choices': [
                    ('Eğer B1, hemen ve açık bir şekilde topun kontrolünü kazanırsa, sesli işaret dikkate alınmayacaktır. Oyun devam edecektir.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-11\nAçıklama: Topu kontrol eden bir takıma pozisyon sırasına topu oyuna sokma hakkı verilirse, bu takımın sadece, hava atışı durumu oluştuğunda şut saatinde kalan süre kadar zamanı olacaktır.\nÖrnek 29/50-12: A takımı, bir hava atışı durumu meydana geldiğinde şut saatinde10 saniyeyle, kendi ön sahasında topu kontrol etmektedir. Pozisyon sırasına göre topu oyuna sokma hakkı: (a) A takımındadır. (b) B takımındadır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) A takımının şut saatinde 10 saniyesi olacaktır. (b) B takımının şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('(a) A takımının şut saatinde 10 saniyesi olacaktır. (b) B takımının şut saatinde 24 saniyesi olacaktır.', True),
                    ('Atış saati 24 saniyeye ayarlanır', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-13\nAçıklama: Eğer oyun, bir hakem tarafından topu kontrol etmeyen takımın yaptığı bir faul ya da ihlal (topun saha dışına çıkma durumu hariç) için durdurulursa ve topu oyuna sokma hakkı, önceden topu ön sahada kontrol eden aynı takımdaysa, şut saati aşağıdaki gibi ayarlanacaktır. • Oyun durdurulduğu zaman şut saati14 saniye ya da daha fazla gösteriyorsa şut saati, kalan süre ile devam edecektir. • Oyun durdurulduğu zaman şut saati13 saniye ya da daha az gösteriyorsa...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun, A takımı tarafından ön sahada topu oyuna sokmasıyla devam edecektir ve A takımının şut saatinde, (a) 8 saniyesi (b) 14 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-13\nAçıklama: Eğer oyun, bir hakem tarafından topu kontrol etmeyen takımın yaptığı bir faul ya da ihlal (topun saha dışına çıkma durumu hariç) için durdurulursa ve topu oyuna sokma hakkı, önceden topu ön sahada kontrol eden aynı takımdaysa, şut saati aşağıdaki gibi ayarlanacaktır. • Oyun durdurulduğu zaman şut saati14 saniye ya da daha fazla gösteriyorsa şut saati, kalan süre ile devam edecektir. • Oyun durdurulduğu zaman şut saati13 saniye ya da daha az gösteriyorsa...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A takımının şut saatinde: (a) 4 saniyesi, (b) 14 saniyesi olacaktır.',
                'choices': [
                    ('A takımının şut saatinde: (a) 4 saniyesi, (b) 14 saniyesi olacaktır.', True),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                    ('Atış saati 24 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-13\nAçıklama: Eğer oyun, bir hakem tarafından topu kontrol etmeyen takımın yaptığı bir faul ya da ihlal (topun saha dışına çıkma durumu hariç) için durdurulursa ve topu oyuna sokma hakkı, önceden topu ön sahada kontrol eden aynı takımdaysa, şut saati aşağıdaki gibi ayarlanacaktır. • Oyun durdurulduğu zaman şut saati14 saniye ya da daha fazla gösteriyorsa şut saati, kalan süre ile devam edecektir. • Oyun durdurulduğu zaman şut saati13 saniye ya da daha az gösteriyorsa...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A takımının şut saatinde, (a) 6 saniyesi (b) 14 saniyesi olacaktır.',
                'choices': [
                    ('A takımının şut saatinde, (a) 6 saniyesi (b) 14 saniyesi olacaktır.', True),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                    ('Atış saati 24 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-13\nAçıklama: Eğer oyun, bir hakem tarafından topu kontrol etmeyen takımın yaptığı bir faul ya da ihlal (topun saha dışına çıkma durumu hariç) için durdurulursa ve topu oyuna sokma hakkı, önceden topu ön sahada kontrol eden aynı takımdaysa, şut saati aşağıdaki gibi ayarlanacaktır. • Oyun durdurulduğu zaman şut saati14 saniye ya da daha fazla gösteriyorsa şut saati, kalan süre ile devam edecektir. • Oyun durdurulduğu zaman şut saati13 saniye ya da daha az gösteriyorsa...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Eşit cezaların iptalinden sonra oyun A takımının topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 5 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-13\nAçıklama: Eğer oyun, bir hakem tarafından topu kontrol etmeyen takımın yaptığı bir faul ya da ihlal (topun saha dışına çıkma durumu hariç) için durdurulursa ve topu oyuna sokma hakkı, önceden topu ön sahada kontrol eden aynı takımdaysa, şut saati aşağıdaki gibi ayarlanacaktır. • Oyun durdurulduğu zaman şut saati14 saniye ya da daha fazla gösteriyorsa şut saati, kalan süre ile devam edecektir. • Oyun durdurulduğu zaman şut saati13 saniye ya da daha az gösteriyorsa...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da bu, topa bilerek ayağıyla tekme attığından ya da topa yumruğuyla vurduğundan dolayı B1’in ihlalidir. Oyun, şut saati, (a) 16 saniye (b) 14 saniye gösterecek şekilde A takımı tarafından, ön sahasından topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-13\nAçıklama: Eğer oyun, bir hakem tarafından topu kontrol etmeyen takımın yaptığı bir faul ya da ihlal (topun saha dışına çıkma durumu hariç) için durdurulursa ve topu oyuna sokma hakkı, önceden topu ön sahada kontrol eden aynı takımdaysa, şut saati aşağıdaki gibi ayarlanacaktır. • Oyun durdurulduğu zaman şut saati14 saniye ya da daha fazla gösteriyorsa şut saati, kalan süre ile devam edecektir. • Oyun durdurulduğu zaman şut saati13 saniye ya da daha az gösteriyorsa...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A2’nin kimse dizilmeden kullandığı 2 serbest atış sonrasında, atışların başarılı olup olmadığına bakılmaksızın oyun, A takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır. Aynı yorum diskalifiye edici faul için de geçerlidir.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-20\nAçıklama: Eğer oyun, bir hakem tarafından iki takımı ilgilendirmeyen herhangi bir geçerli nedenle durdurulursa ve hakemlerin değerlendirmesine göre rakipler dezavantajlı bir duruma düşerse şut saati kalan süre ile devam edecektir.\nÖrnek 29/50-21: Dördüncü çeyrekte oyun saatinde 0:25 kala ve skor A 72 – B 72 iken A takımı, kendi ön sahasında topun kontrolünü kazanır. Oyun, hakemler tarafından aşağıdaki nedenlerden dolayı durdurulduğunda A1, 20 saniye boyunca dripl...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda oyun, oyunun durdurulduğu en yakın yerden A takımının topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 4 saniyesi olacaktır. Eğer oyun, şut saatinde kalan süre olmadan devam ederse B takımı dezavantajlı duruma düşecektir.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-20\nAçıklama: Eğer oyun, bir hakem tarafından iki takımı ilgilendirmeyen herhangi bir geçerli nedenle durdurulursa ve hakemlerin değerlendirmesine göre rakipler dezavantajlı bir duruma düşerse şut saati kalan süre ile devam edecektir.\nÖrnek 29/50-22: A1’in sayı amacıyla attığı şut çembere temas eder. A2 ribaundu alır ve 9 saniye sonra şut saati yanlışlıkla sesli işaret verir. Hakemler oyunu durdururlar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Eğer bu bir şut saati ihlali olursa, topu kontrol eden A takımı dezavantajlı duruma düşecektir. Hakemler, varsa komisere ve şut saati görevlisine danıştıktan sonra oyun A takımının topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 5 saniyesi olacaktır.',
                'choices': [
                    ('Şut saati ihlali: Top A takımına verilir', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-20\nAçıklama: Eğer oyun, bir hakem tarafından iki takımı ilgilendirmeyen herhangi bir geçerli nedenle durdurulursa ve hakemlerin değerlendirmesine göre rakipler dezavantajlı bir duruma düşerse şut saati kalan süre ile devam edecektir.\nÖrnek 29/50-23: Şut saatinde 4 saniye kala A1 sayı amacıyla bir şut atar. Top çembere temas etmez ancak şut saati görevlisi yanlışlıkla saati başa alır. A2 ribaundu alır ve bir süre sonra A3 sayı kaydeder. Bu sırada hakemler hatayı fark...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Hakemler, varsa komisere danıştıktan sonra A1’in şutunda topun çembere temas etmediğini teyit edecektir. Şut saatini başa alma durumu olmasaydı şut saatinin sesli işaretinden önce topun, A3’ün el ya da ellerini terk edip etmediğine karar vereceklerdir. Eğer topun ellerini terk ettiğine karar verilirse, A3’ün sayısı sayı geçerli olacaktır. Aksi takdirde bir şut saati ihlali olacak ve A3’ün sayısı geçerli olmayacaktır.',
                'choices': [
                    ('Şut saati ihlali', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-24\nAçıklama: Sayı amacıyla atılan bir şut elden çıktıktan sonra kendi geri sahasında olan bir savunma oyuncusuna faul çalınır. Oyun topun oyuna sokulmasıyla devam edecekse şut saati aşağıdaki şekilde ayarlanacaktır. • Eğer oyun durdurulduğu anda şut saati 14 saniye veya daha fazla gösteriyorsa şut saati başa alınmayacak, durdurulduğu yerden itibaren devam edecektir. • Eğer oyun durdurulduğu anda şut saati 13 saniye veya daha az gösteriyorsa şut saati 14 saniyeye aya...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in sayısı geçerlidir. Oyun A takımı tarafından B2’nin faulünün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-24\nAçıklama: Sayı amacıyla atılan bir şut elden çıktıktan sonra kendi geri sahasında olan bir savunma oyuncusuna faul çalınır. Oyun topun oyuna sokulmasıyla devam edecekse şut saati aşağıdaki şekilde ayarlanacaktır. • Eğer oyun durdurulduğu anda şut saati 14 saniye veya daha fazla gösteriyorsa şut saati başa alınmayacak, durdurulduğu yerden itibaren devam edecektir. • Eğer oyun durdurulduğu anda şut saati 13 saniye veya daha az gösteriyorsa şut saati 14 saniyeye aya...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda oyun A takımı tarafından, kendi ön sahasındaki B2’nin faulünün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 17 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-24\nAçıklama: Sayı amacıyla atılan bir şut elden çıktıktan sonra kendi geri sahasında olan bir savunma oyuncusuna faul çalınır. Oyun topun oyuna sokulmasıyla devam edecekse şut saati aşağıdaki şekilde ayarlanacaktır. • Eğer oyun durdurulduğu anda şut saati 14 saniye veya daha fazla gösteriyorsa şut saati başa alınmayacak, durdurulduğu yerden itibaren devam edecektir. • Eğer oyun durdurulduğu anda şut saati 13 saniye veya daha az gösteriyorsa şut saati 14 saniyeye aya...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) A1’in sayısı geçerlidir. Tüm durumlarda oyun A takımı tarafından, kendi ön sahasındaki B2’nin faulünün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-24\nAçıklama: Sayı amacıyla atılan bir şut elden çıktıktan sonra kendi geri sahasında olan bir savunma oyuncusuna faul çalınır. Oyun topun oyuna sokulmasıyla devam edecekse şut saati aşağıdaki şekilde ayarlanacaktır. • Eğer oyun durdurulduğu anda şut saati 14 saniye veya daha fazla gösteriyorsa şut saati başa alınmayacak, durdurulduğu yerden itibaren devam edecektir. • Eğer oyun durdurulduğu anda şut saati 13 saniye veya daha az gösteriyorsa şut saati 14 saniyeye aya...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) A1’in sayısı geçerlidir. Tüm durumlarda bu, A takımının şut saati ihlali değildir. Oyun A takımı tarafından, kendi ön sahasındaki B2’nin faulünün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Şut saati ihlali: Top A takımına verilir', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-24\nAçıklama: Sayı amacıyla atılan bir şut elden çıktıktan sonra kendi geri sahasında olan bir savunma oyuncusuna faul çalınır. Oyun topun oyuna sokulmasıyla devam edecekse şut saati aşağıdaki şekilde ayarlanacaktır. • Eğer oyun durdurulduğu anda şut saati 14 saniye veya daha fazla gösteriyorsa şut saati başa alınmayacak, durdurulduğu yerden itibaren devam edecektir. • Eğer oyun durdurulduğu anda şut saati 13 saniye veya daha az gösteriyorsa şut saati 14 saniyeye aya...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) A1’in sayısı geçerlidir. Tüm durumlarda A2, 2 serbest atış kullanacaktır. Oyun herhangi bir son serbest atış sonrası olduğu gibi devam edecektir.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-24\nAçıklama: Sayı amacıyla atılan bir şut elden çıktıktan sonra kendi geri sahasında olan bir savunma oyuncusuna faul çalınır. Oyun topun oyuna sokulmasıyla devam edecekse şut saati aşağıdaki şekilde ayarlanacaktır. • Eğer oyun durdurulduğu anda şut saati 14 saniye veya daha fazla gösteriyorsa şut saati başa alınmayacak, durdurulduğu yerden itibaren devam edecektir. • Eğer oyun durdurulduğu anda şut saati 13 saniye veya daha az gösteriyorsa şut saati 14 saniyeye aya...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) A1’in sayısı geçerlidir. Tüm durumlarda bu A takımının şut saati ihlali değildir. A2, 2 serbest atış kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir.',
                'choices': [
                    ('Şut saati ihlali: Top A takımına verilir', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-24\nAçıklama: Sayı amacıyla atılan bir şut elden çıktıktan sonra kendi geri sahasında olan bir savunma oyuncusuna faul çalınır. Oyun topun oyuna sokulmasıyla devam edecekse şut saati aşağıdaki şekilde ayarlanacaktır. • Eğer oyun durdurulduğu anda şut saati 14 saniye veya daha fazla gösteriyorsa şut saati başa alınmayacak, durdurulduğu yerden itibaren devam edecektir. • Eğer oyun durdurulduğu anda şut saati 13 saniye veya daha az gösteriyorsa şut saati 14 saniyeye aya...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Her iki durumda da A (B2’nin teknik faulü için) veya B (A2’nin teknik faulü için) takımının herhangi bir oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. (a) A1'in sayısı geçerli sayılacaktır. Oyun B takımı tarafından kendi dip çizgisinin gerisinden topu oyuna sokmasıyla devam edecektir. (b) Bu bir hava atışı durumudur. Oyun şu şekilde devam edecektir; Pozisyon sırası A takımı gösteriyorsa bu durum, A takımının şut saati ihlalidir. Top, şut saatinde 24 saniye ile kendi geri sahasından topu oyuna sokması için B takımına verilecektir. Pozisyon sırası B takımını gösteriyorsa top, şut saatinde 24 saniye ile kendi geri sahasından topu oyuna sokması için B takımına verilecektir.",
                'choices': [
                    ('Şut saati ihlali: Top B takımına verilir', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-32\nAçıklama: Bir sportmenlik dışı ya da bir diskalifiye edici faulün cezası sonucu topun oyuna sokulması, her zaman takımın ön sahasındaki topu oyuna sokma çizgisinden yönetilecektir. Takımın şut saatinde 14 saniyesi olacaktır.\nÖrnek 29/50-33: Dördüncü çeyrekte oyun saatinde 1:12 ve şut saatinde 6 saniye kala A1 ön sahasında dripling yaparken B1, A1’e bir sportmenlik dışı faul yapar. A1’in ilk serbest atışından sonra A takımı ya da B takımı başantrenörü mola ister.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1, kimse dizilmeden ikinci serbest atışını kullanacaktır. Daha sonrasında mola verilecektir. Moladan sonra oyun A takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': "Madde 29/50 Şut saati | 29/50-32\nAçıklama: Bir sportmenlik dışı ya da bir diskalifiye edici faulün cezası sonucu topun oyuna sokulması, her zaman takımın ön sahasındaki topu oyuna sokma çizgisinden yönetilecektir. Takımın şut saatinde 14 saniyesi olacaktır.\nÖrnek 29/50-34: Şut saatinde 19 saniye kala B2, A2'ye bir sportmenlik dışı faulle yaptığında A1 kendi ön sahasında dripling yapmaktadır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'A2’nin kimse dizilmeden kullandığı 2 serbest atış sonrasında, atışların başarılı olup olmamasına bakılmaksızın oyun A takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır. Aynı yorum diskalifiye edici faul için de geçerlidir.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-35\nAçıklama: Top, herhangi bir nedenle rakibin çemberine temas ettikten sonra topun kontrolünü kazanan takım, top çembere temas etmeden önce topu kontrol eden aynı takımsa şut saati 14 saniyeye ayarlanacaktır.\nÖrnek 29/50-36: A1’in A2’ye pası sırasında top B2’ye temas eder ve ardından çembere temas eder. A3 topun kontrolünü kazanır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A3 sahanın herhangi bir yerinde topun kontrolünü kazandığında, A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('A3 sahanın herhangi bir yerinde topun kontrolünü kazandığında, A takımının şut saatinde 14 saniyesi olacaktır.', True),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                    ('Atış saati 24 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-35\nAçıklama: Top, herhangi bir nedenle rakibin çemberine temas ettikten sonra topun kontrolünü kazanan takım, top çembere temas etmeden önce topu kontrol eden aynı takımsa şut saati 14 saniyeye ayarlanacaktır.\nÖrnek 29/50-37: A1 sayı amacıyla bir şut girişiminde bulunur, şut saatinde, (a) 4 saniye, (b) 20 saniye kala. Top çembere temas eder, A2 ribaundu alır ve topun kontrolünü kazanır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da A2, oyun sahasının herhangi bir yerinde topun kontrolünü kazandığında, A takımının şut saatinde14 saniyesi olacaktır.',
                'choices': [
                    ('Her iki durumda da A2, oyun sahasının herhangi bir yerinde topun kontrolünü kazandığında, A takımının şut saatinde14 saniyesi olacaktır.', True),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                    ('Atış saati 24 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-35\nAçıklama: Top, herhangi bir nedenle rakibin çemberine temas ettikten sonra topun kontrolünü kazanan takım, top çembere temas etmeden önce topu kontrol eden aynı takımsa şut saati 14 saniyeye ayarlanacaktır.\nÖrnek 29/50-38: A1 sayı amacıyla bir şut girişiminde bulunur. Top çembere temas eder. (a) B1 topa temas eder (b) A2 topu tipler ve ardından A3 topun kontrolünü kazanır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da A3 sahanın herhangi bir yerinde topun kontrolünü kazandığında A takımının şut saatinde 14 saniyesi olacaktır',
                'choices': [
                    ('Her iki durumda da A3 sahanın herhangi bir yerinde topun kontrolünü kazandığında A takımının şut saatinde 14 saniyesi olacaktır', True),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                    ('Atış saati 24 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-35\nAçıklama: Top, herhangi bir nedenle rakibin çemberine temas ettikten sonra topun kontrolünü kazanan takım, top çembere temas etmeden önce topu kontrol eden aynı takımsa şut saati 14 saniyeye ayarlanacaktır.\nÖrnek 29/50-39: A1 sayı amacıyla bir şut girişiminde bulunur. Top çembere temas eder. B1 daha sonra top saha dışına çıkmadan önce topa temas eder.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun topun saha dışına çıktığı en yakın yerden A takımının topu oyuna sokmasıyla devam edecektir. Topun oyuna sokulmasının oyun sahasının neresinden yönetileceğine bakılmaksızın A takımının şut saatinde14 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-35\nAçıklama: Top, herhangi bir nedenle rakibin çemberine temas ettikten sonra topun kontrolünü kazanan takım, top çembere temas etmeden önce topu kontrol eden aynı takımsa şut saati 14 saniyeye ayarlanacaktır.\nÖrnek 29/50-40: Şut saatinde 4 saniye kala A1, şut saatinin başa alınması için topu çembere doğru atar. Top çembere temas eder. B1 daha sonra A takımının geri sahasından top saha dışına çıkmadan topa temas eder.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun, A takımının kendi geri sahasından, topun saha dışına çıktığı en yakın yerden topun oyuna sokulmasıyla devam edecektir. A takımının şut saatinde14 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-35\nAçıklama: Top, herhangi bir nedenle rakibin çemberine temas ettikten sonra topun kontrolünü kazanan takım, top çembere temas etmeden önce topu kontrol eden aynı takımsa şut saati 14 saniyeye ayarlanacaktır.\nÖrnek 29/50-41: Şut saatinde 6 saniye kala A1 sayı amacıyla bir şut girişiminde bulunur. Top çembere temas eder ve ardından A2 topun kontrolünü kazanır. Daha sonra B2, A2’ye ribaund sırasında bir faul yapar. Bu B takımının o çeyrekteki üçüncü takım faulüdür.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Oyun A takımın tarafından B2'nin faulünün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.",
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-35\nAçıklama: Top, herhangi bir nedenle rakibin çemberine temas ettikten sonra topun kontrolünü kazanan takım, top çembere temas etmeden önce topu kontrol eden aynı takımsa şut saati 14 saniyeye ayarlanacaktır.\nÖrnek 29/50-42: A1 sayı amacıyla bir şut girişiminde bulunur. Top çembere temas eder ve ribaund sırasında A2 ile B2 arasında bir tutulmuş top kararı verilir. Pozisyon sırası oku A takımını gösterir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun tutulmuş top durumunun meydana geldiği en yakın yerden A takımının topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde14 saniyesi olacaktır.',
                'choices': [
                    ('Tutulmuş top', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-35\nAçıklama: Top, herhangi bir nedenle rakibin çemberine temas ettikten sonra topun kontrolünü kazanan takım, top çembere temas etmeden önce topu kontrol eden aynı takımsa şut saati 14 saniyeye ayarlanacaktır.\nÖrnek 29/50-43: A1 sayı amacıyla bir şut girişiminde bulunur, şut saatinde: (a) 8 saniye, (b) 17 saniye kala. Top çemberle arkalık arasına sıkışır. Pozisyon sırası oku A takımını gösterir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da oyun A takımı tarafından kendi ön sahasındaki dip çizginin gerisinden, arkalığa en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde14 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-35\nAçıklama: Top, herhangi bir nedenle rakibin çemberine temas ettikten sonra topun kontrolünü kazanan takım, top çembere temas etmeden önce topu kontrol eden aynı takımsa şut saati 14 saniyeye ayarlanacaktır.\nÖrnek 29/50-44: A1 ön sahada smaç yapması için topu pas olarak atar ama A2 pası tutamaz. Top çembere temas eder ve sonrasında A3 topun kontrolünü A takımının; (a) ön sahasında (b) geri sahasında kazanır\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) A takımının şut saatinde 14 saniyesi olacaktır. (b) A takımı topun kontrolünü kaybetmediği için bu A takımının geri saha ihlalidir.',
                'choices': [
                    ('(a) A takımının şut saatinde 14 saniyesi olacaktır. (b) A takımı topun kontrolünü kaybetmediği için bu A takımının geri saha ihlalidir.', True),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                    ('Atış saati 24 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-35\nAçıklama: Top, herhangi bir nedenle rakibin çemberine temas ettikten sonra topun kontrolünü kazanan takım, top çembere temas etmeden önce topu kontrol eden aynı takımsa şut saati 14 saniyeye ayarlanacaktır.\nÖrnek 29/50-45: A1’in sayı amacıyla attığı şut çembere temas eder. B1 ribaundu alır ve sahaya geri döner. A2, B1’in elindeki topa vurur. Sonrasında A3 topu yakalar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B takımı (B1) ribaund sırasında topun açık kontrolünü kazanmıştır, ardından A takımı (A3) yeni bir kontrol kazanır. A takımının şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('B takımı (B1) ribaund sırasında topun açık kontrolünü kazanmıştır, ardından A takımı (A3) yeni bir kontrol kazanır. A takımının şut saatinde 24 saniyesi olacak…', True),
                    ('Atış saati 24 saniyeye ayarlanır', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-35\nAçıklama: Top, herhangi bir nedenle rakibin çemberine temas ettikten sonra topun kontrolünü kazanan takım, top çembere temas etmeden önce topu kontrol eden aynı takımsa şut saati 14 saniyeye ayarlanacaktır.\nÖrnek 29/50-46: Şut saatinde 5 saniye kala topu oyuna sokan A1 topu pas olarak B takımının sepetine doğru atar. Top çembere temas eder ve ardından A2 ve / veya B2 tarafından topa temas edilir fakat kontrol edilemez.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Sahadaki herhangi bir oyuncu topa dokunduğunda ya da top herhangi bir oyuncuya temas ettiğinden oyun saati ve şut saati aynı anda başlatılacaktır. Eğer A takımı sahada topun kontrolünü kazanırsa şut saatinde 14 saniyesi olacaktır. Eğer B takımı sahada topun kontrolünü kazanırsa şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('Sahadaki herhangi bir oyuncu topa dokunduğunda ya da top herhangi bir oyuncuya temas ettiğinden oyun saati ve şut saati aynı anda başlatılacaktır. Eğer A takım…', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-47\nAçıklama: Oyun sırasında oyun saati çalışırken bir takım, ön sahasında ya da geri sahasında canlı bir topun kontrolünü yeniden kazandığında o takımın şut saatinde 24 saniyesi olacaktır.\nÖrnek 29/50-48: Oyun saati çalışırken A1 oyun sahasında yeni bir top kontrolünü kazanır (a) Geri sahada (b) Ön sahada\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da A takımın şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('Her iki durumda da A takımın şut saatinde 24 saniyesi olacaktır.', True),
                    ('Atış saati 24 saniyeye ayarlanır', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-47\nAçıklama: Oyun sırasında oyun saati çalışırken bir takım, ön sahasında ya da geri sahasında canlı bir topun kontrolünü yeniden kazandığında o takımın şut saatinde 24 saniyesi olacaktır.\nÖrnek 29/50-49: B takımının topu oyuna sokmasından sonra A1 oyun sahasındaki topun kontrolünü hemen ve açık bir şekilde kazanır. (a) Geri sahada (b) Ön sahada\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da A takımının şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('Her iki durumda da A takımının şut saatinde 24 saniyesi olacaktır.', True),
                    ('Atış saati 24 saniyeye ayarlanır', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': "Madde 29/50 Şut saati | 29/50-50\nAçıklama: Oyun, topu kontrol eden takımın yaptığı bir faul veya ihlal (saha dışına çıkan top dahil) nedeniyle hakem tarafından durdurulur. Eğer top ön sahasından topu oyuna sokacak olan rakibe verilirse o takımın şut saatinde 14 saniyesi olacaktır.\nÖrnek 29/50-51: Geri saha içerisinde A1, A2'ye pas verir. A2 topa temas eder ancak A takımının geri sahasından saha dışına çıkmadan önce topu yakalayamaz.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Oyun B takımının ön sahasında, topun saha dışına çıktığı en yakın yerden topun oyuna sokulmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-52\nAçıklama: Bir takım sahanın herhangi bir yerinde oyun saatinde 24 saniyeden daha az varken yeni bir top kontrolü kazandığında veya canlı bir topun kontrolünü tekrar geri kazandığında, şut saati görüntüsü kapatılacaktır. Top rakibin çemberine değdikten sonra ve bir takım oyun saatinde 24 saniyeden az ve 14 saniyeden fazla bir süre varken canlı bir topun kontrolünü oyun sahasının herhangi bir yerinde yeniden/tekrardan kazandığında takımın şut saatinde 14 saniyesi o...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Şut saati görüntüsü kapatılacaktır.',
                'choices': [
                    ('Şut saati görüntüsü kapatılacaktır.', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-52\nAçıklama: Bir takım sahanın herhangi bir yerinde oyun saatinde 24 saniyeden daha az varken yeni bir top kontrolü kazandığında veya canlı bir topun kontrolünü tekrar geri kazandığında, şut saati görüntüsü kapatılacaktır. Top rakibin çemberine değdikten sonra ve bir takım oyun saatinde 24 saniyeden az ve 14 saniyeden fazla bir süre varken canlı bir topun kontrolünü oyun sahasının herhangi bir yerinde yeniden/tekrardan kazandığında takımın şut saatinde 14 saniyesi o...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Oyun A takımı tarafından ön sahasından, B1'in topa vurduğu en yakın yerden topu oyuna sokmasıyla devam edecektir. Oyun saati 18 saniyeyi gösterecektir. Şut saati görüntüsü kapatılacaktır.",
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-52\nAçıklama: Bir takım sahanın herhangi bir yerinde oyun saatinde 24 saniyeden daha az varken yeni bir top kontrolü kazandığında veya canlı bir topun kontrolünü tekrar geri kazandığında, şut saati görüntüsü kapatılacaktır. Top rakibin çemberine değdikten sonra ve bir takım oyun saatinde 24 saniyeden az ve 14 saniyeden fazla bir süre varken canlı bir topun kontrolünü oyun sahasının herhangi bir yerinde yeniden/tekrardan kazandığında takımın şut saatinde 14 saniyesi o...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun, oyun saatinde 16 saniye ile devam edecektir. Şut saati açılacaktır. A takımı topun kontrolünü yeniden kazandığında oyun saatinde 14 saniyeden fazla süre olduğundan, A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Oyun, oyun saatinde 16 saniye ile devam edecektir. Şut saati açılacaktır. A takımı topun kontrolünü yeniden kazandığında oyun saatinde 14 saniyeden fazla süre …', True),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                    ('Atış saati 24 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-52\nAçıklama: Bir takım sahanın herhangi bir yerinde oyun saatinde 24 saniyeden daha az varken yeni bir top kontrolü kazandığında veya canlı bir topun kontrolünü tekrar geri kazandığında, şut saati görüntüsü kapatılacaktır. Top rakibin çemberine değdikten sonra ve bir takım oyun saatinde 24 saniyeden az ve 14 saniyeden fazla bir süre varken canlı bir topun kontrolünü oyun sahasının herhangi bir yerinde yeniden/tekrardan kazandığında takımın şut saatinde 14 saniyesi o...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun A takımı tarafından ön sahasından topun saha dışına çıktığı en yakın yerden oyun saatinde 12 saniyeyle topu oyuna sokmasıyla devam edecektir. A takımı topun kontrolünü yeniden kazandığında oyun saatinde 14 saniyeden az süre kaldığı için şut saati görüntüsü kapalı kalmaya devam edecektir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-52\nAçıklama: Bir takım sahanın herhangi bir yerinde oyun saatinde 24 saniyeden daha az varken yeni bir top kontrolü kazandığında veya canlı bir topun kontrolünü tekrar geri kazandığında, şut saati görüntüsü kapatılacaktır. Top rakibin çemberine değdikten sonra ve bir takım oyun saatinde 24 saniyeden az ve 14 saniyeden fazla bir süre varken canlı bir topun kontrolünü oyun sahasının herhangi bir yerinde yeniden/tekrardan kazandığında takımın şut saatinde 14 saniyesi o...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun A takımı tarafından ön sahasından topun saha dışına çıktığı en yakın yerden oyun saatinde15.5 saniyeyle topu oyuna sokmasıyla devam edecektir. Şut saati görüntüsü kapalı kalmaya devam edecektir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 29/50 Şut saati | 29/50-52\nAçıklama: Bir takım sahanın herhangi bir yerinde oyun saatinde 24 saniyeden daha az varken yeni bir top kontrolü kazandığında veya canlı bir topun kontrolünü tekrar geri kazandığında, şut saati görüntüsü kapatılacaktır. Top rakibin çemberine değdikten sonra ve bir takım oyun saatinde 24 saniyeden az ve 14 saniyeden fazla bir süre varken canlı bir topun kontrolünü oyun sahasının herhangi bir yerinde yeniden/tekrardan kazandığında takımın şut saatinde 14 saniyesi o...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun, A takımı tarafından ön sahasından, topun saha dışına çıktığı en yakın yerden oyun saatinde12 saniyeyle topu oyuna sokmasıyla devam edecektir. A takımı oyun saatinde 24 saniyeden daha az bir süre kala yeni bir top kontrolü kazandığından şut saati görüntüsü kapalı kalmaya devam edecektir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-1\nAçıklama: Havadaki bir oyuncu havaya sıçramadan önce sahada son temas ettiği yerdeki statüsünü korur. Bununla birlikte bir oyuncu ön sahasından sıçradığında ve hala havadayken takımı için yeni bir top kontrolünü kazandığında bu oyuncu daha sonra topla birlikte sahanın herhangi bir yerine inebilir. Yere inmeden önce geri sahasındaki bir takım arkadaşına pas veremez.\nÖrnek 30-2: Geri sahasındaki A1 ön sahasındaki A2’ye topu pas olarak atar. B1 ön sahasından sı...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu B takımının geri saha ihlali değildir. B1 havadayken B takımı için yeni bir top kontrolünü sağlamıştır ve oyun sahasının herhangi bir yerine inebilir. Tüm durumlarda B1 kurallara uygun olarak geri sahasındadır.',
                'choices': [
                    ('Bu B takımının geri saha ihlali değildir. B1 havadayken B takımı için yeni bir top kontrolünü sağlamıştır ve oyun sahasının herhangi bir yerine inebilir. Tüm d…', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-1\nAçıklama: Havadaki bir oyuncu havaya sıçramadan önce sahada son temas ettiği yerdeki statüsünü korur. Bununla birlikte bir oyuncu ön sahasından sıçradığında ve hala havadayken takımı için yeni bir top kontrolünü kazandığında bu oyuncu daha sonra topla birlikte sahanın herhangi bir yerine inebilir. Yere inmeden önce geri sahasındaki bir takım arkadaşına pas veremez.\nÖrnek 30-3: A1 ile B1 arasındaki oyunun başlangıcı için olan hava atışında top kurallara uygun...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu, A2’nin geri saha ihlali değildir. A2 havadayken A takımı için ilk top kontrolünü sağlamıştır ve oyun sahasının herhangi bir yerine inebilir. Tüm durumlarda A2 kurallara uygun olarak geri sahasındadır.',
                'choices': [
                    ('Bu, A2’nin geri saha ihlali değildir. A2 havadayken A takımı için ilk top kontrolünü sağlamıştır ve oyun sahasının herhangi bir yerine inebilir. Tüm durumlarda…', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-1\nAçıklama: Havadaki bir oyuncu havaya sıçramadan önce sahada son temas ettiği yerdeki statüsünü korur. Bununla birlikte bir oyuncu ön sahasından sıçradığında ve hala havadayken takımı için yeni bir top kontrolünü kazandığında bu oyuncu daha sonra topla birlikte sahanın herhangi bir yerine inebilir. Yere inmeden önce geri sahasındaki bir takım arkadaşına pas veremez.\nÖrnek 30-4: Ön sahasından topu oyuna sokan A1, A2’ye topu pas olarak atar. A2 ön sahasından sı...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A takımının geri saha ihlalidir. A2 havadayken topu yakalayıp geri sahasına inmeden önce topu oyuna sokan A1, A takımının ön sahasında top kontrolünü sağlamıştır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-1\nAçıklama: Havadaki bir oyuncu havaya sıçramadan önce sahada son temas ettiği yerdeki statüsünü korur. Bununla birlikte bir oyuncu ön sahasından sıçradığında ve hala havadayken takımı için yeni bir top kontrolünü kazandığında bu oyuncu daha sonra topla birlikte sahanın herhangi bir yerine inebilir. Yere inmeden önce geri sahasındaki bir takım arkadaşına pas veremez.\nÖrnek 30-5: Geri sahasından topu oyuna sokan A1, ön sahasındaki A2’ye topu pas olarak atar. B1...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu B takımının geri saha ihlalidir. B1 ön sahadan sıçradığında ve havadayken yeni bir takım kontrolü kazandığında B1 sahanın herhangi bir yerine inebilir. Ancak B1 geri sahasındaki bir takım arkadaşına topu pas olarak veremez.',
                'choices': [
                    ('Bu B takımının geri saha ihlalidir. B1 ön sahadan sıçradığında ve havadayken yeni bir takım kontrolü kazandığında B1 sahanın herhangi bir yerine inebilir. Anca…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-1\nAçıklama: Havadaki bir oyuncu havaya sıçramadan önce sahada son temas ettiği yerdeki statüsünü korur. Bununla birlikte bir oyuncu ön sahasından sıçradığında ve hala havadayken takımı için yeni bir top kontrolünü kazandığında bu oyuncu daha sonra topla birlikte sahanın herhangi bir yerine inebilir. Yere inmeden önce geri sahasındaki bir takım arkadaşına pas veremez.\nÖrnek 30-6: A1 ve B1 arasında oyunun başlangıcı için olan hava atışı sırasında top kurallara u...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A takımının geri saha ihlalidir. A2 havadayken elinde topla kendi geri sahasına inebilir ancak geri sahasındaki takım arkadaşına topu pas olarak veremez.',
                'choices': [
                    ('Bu A takımının geri saha ihlalidir. A2 havadayken elinde topla kendi geri sahasına inebilir ancak geri sahasındaki takım arkadaşına topu pas olarak veremez.', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-7\nAçıklama: Tamamen ön sahasında olan bir A takımı oyuncusu topun kendi geri sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oyuncu olursa, canlı bir top kural dışı olarak geri sahaya dönmüştür. Ancak, geri sahasındaki bir A takımı oyuncusu topun ön sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A takımının geri saha ihlalidir.',
                'choices': [
                    ('Bu A takımının geri saha ihlalidir.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-7\nAçıklama: Tamamen ön sahasında olan bir A takımı oyuncusu topun kendi geri sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oyuncu olursa, canlı bir top kural dışı olarak geri sahaya dönmüştür. Ancak, geri sahasındaki bir A takımı oyuncusu topun ön sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A takımının ön sahasında topla birlikte bir A takımı oyuncusu olmadığından geri saha ihlali olmamıştır. Ancak 8 saniye sayımı top A takımının ön sahasına temas ettiğinde durdurulacaktır. A2 geri sahasında topa temas eder etmez, yeni bir 8 saniye sayımı başlatılacaktır.',
                'choices': [
                    ('A takımının ön sahasında topla birlikte bir A takımı oyuncusu olmadığından geri saha ihlali olmamıştır. Ancak 8 saniye sayımı top A takımının ön sahasına temas…', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-7\nAçıklama: Tamamen ön sahasında olan bir A takımı oyuncusu topun kendi geri sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oyuncu olursa, canlı bir top kural dışı olarak geri sahaya dönmüştür. Ancak, geri sahasındaki bir A takımı oyuncusu topun ön sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Hiçbir A takımı oyuncusu ön sahada topun kontrolüne sahip olmadığından bu A takımı tarafından yapılan bir geri saha ihlali değildir. Ancak top, orta çizginin iki yanında olarak sahada duran bir hakeme temas ettiğinde 8 saniye sayımı durdurulacaktır. A2 geri sahasında topa temas eder etmez yeni bir 8 saniye sayımı başlatılacaktır.',
                'choices': [
                    ('Hiçbir A takımı oyuncusu ön sahada topun kontrolüne sahip olmadığından bu A takımı tarafından yapılan bir geri saha ihlali değildir. Ancak top, orta çizginin i…', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-7\nAçıklama: Tamamen ön sahasında olan bir A takımı oyuncusu topun kendi geri sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oyuncu olursa, canlı bir top kural dışı olarak geri sahaya dönmüştür. Ancak, geri sahasındaki bir A takımı oyuncusu topun ön sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A takımının geri saha ihlalidir.',
                'choices': [
                    ('Bu A takımının geri saha ihlalidir.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-7\nAçıklama: Tamamen ön sahasında olan bir A takımı oyuncusu topun kendi geri sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oyuncu olursa, canlı bir top kural dışı olarak geri sahaya dönmüştür. Ancak, geri sahasındaki bir A takımı oyuncusu topun ön sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A takımının kurallara uygun bir oyunudur. A1 kendi ön sahasında topun kontrolünü henüz sağlamamıştır.',
                'choices': [
                    ('Bu A takımının kurallara uygun bir oyunudur. A1 kendi ön sahasında topun kontrolünü henüz sağlamamıştır.', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-7\nAçıklama: Tamamen ön sahasında olan bir A takımı oyuncusu topun kendi geri sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oyuncu olursa, canlı bir top kural dışı olarak geri sahaya dönmüştür. Ancak, geri sahasındaki bir A takımı oyuncusu topun ön sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A takımının kurallara uygun bir oyunudur. A2 kendi ön sahasında topun kontrolünü henüz sağlamamıştır.',
                'choices': [
                    ('Bu A takımının kurallara uygun bir oyunudur. A2 kendi ön sahasında topun kontrolünü henüz sağlamamıştır.', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-7\nAçıklama: Tamamen ön sahasında olan bir A takımı oyuncusu topun kendi geri sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oyuncu olursa, canlı bir top kural dışı olarak geri sahaya dönmüştür. Ancak, geri sahasındaki bir A takımı oyuncusu topun ön sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A takımının geri saha ihlalidir. Topu oyuna sokan A1, A takımının ön sahasında takım kontrolünü zaten sağlamıştı.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-7\nAçıklama: Tamamen ön sahasında olan bir A takımı oyuncusu topun kendi geri sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oyuncu olursa, canlı bir top kural dışı olarak geri sahaya dönmüştür. Ancak, geri sahasındaki bir A takımı oyuncusu topun ön sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A takımının kurallara uygun bir oyunudur. A1 ön sahasında topa son dokunan oyuncu değildir. A1 geri sahasında tamamen yeni bir 8 saniye süresiyle driplingine devam bile edebilir.',
                'choices': [
                    ('Bu A takımının kurallara uygun bir oyunudur. A1 ön sahasında topa son dokunan oyuncu değildir. A1 geri sahasında tamamen yeni bir 8 saniye süresiyle driplingin…', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 30 Geri sahaya dönen top | 30-7\nAçıklama: Tamamen ön sahasında olan bir A takımı oyuncusu topun kendi geri sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oyuncu olursa, canlı bir top kural dışı olarak geri sahaya dönmüştür. Ancak, geri sahasındaki bir A takımı oyuncusu topun ön sahasına temas etmesine neden olduğunda, bundan sonra bir A takımı oyuncusu ön sahasında ya da geri sahasında topa temas eden ilk oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda bu A takımının geri saha ihlalidir. A2 havadayken, A takımının ön sahasındaki takım kontrolünü sağlamıştır.',
                'choices': [
                    ('Tüm durumlarda bu A takımının geri saha ihlalidir. A2 havadayken, A takımının ön sahasındaki takım kontrolünü sağlamıştır.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-1\nAçıklama: Sayı amacıyla yapılan bir şut ya da bir serbest atış girişimi sırasında top çemberin üzerindeyken bir oyuncunun sepete doğru alttan uzanıp topa dokunması bir müdahale ihlalidir.\nÖrnek 31-2: A1’in son serbest atışı sırasında, (a) Top çembere temas etmeden önce, (b) Top çembere temas ettikten sonra ve hala sepete girme olasılığı varken, B1 sepete doğru alttan uzanır ve topa temas eder.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da bu B1 tarafından yapılan bir topa müdahale ihlalidir. A1’e 1 sayı verilecek ve, (a) B1’e bir teknik faul verilecektir. (b) B1’e bir teknik faul verilmeyecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-3\nAçıklama: Bir pas sırasında ya da çembere temas ettikten sonra top çemberin üzerindeyken bir oyuncunun sepete doğru alttan uzanıp topa dokunması bir müdahaledir.\nÖrnek 31-4: B1 sepete doğru alttan uzanıp topa temas ettiğinde top, A1’in bir pası sonucunda çemberin üzerindedir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu, B1 tarafından yapılan bir müdahale ihlalidir. A1’e 2 ya da 3 sayı verilecektir.',
                'choices': [
                    ('Bu, B1 tarafından yapılan bir müdahale ihlalidir. A1’e 2 ya da 3 sayı verilecektir.', True),
                    ('Bu, B1 tarafından yapılan bir müdahale ihlalidir. A1’e 2 ya da 3 sayı verilmeyecektir.', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-5\nAçıklama: Başarısız bir son serbest atış sonrasında top çembere temas eder. Top sepete girmeden önce herhangi bir oyuncu tarafından topa kurallara uygun olarak temas edilirse serbest atış 2 sayılık olarak değerlendirilir.\nÖrnek 31-6: A1’in son serbest atışından sonra top çembere temas eder ve üzerinde yükselir. B1 topu uzağa tiplemeye çalışır ancak top sepete girer.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Bu durum B1'in kurallara uygun olarak topu kendi sepetine doğru tiplemesidir. A takımının oyun sahasındaki kaptanına 2 sayı verilecektir.",
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': "Madde 31 Sayıya yönelen top ve müdahale | 31-7\nAçıklama: Aşağıdaki durumlarda top çembere temas ettikten sonra ve topun hala sepete girme olasılığı varken bir faul çalınır. • sayı amacıyla bir şut girişiminde, • başarısız bir son serbest atışta, • oyun saati çeyreğin ya da uzatmanın sonu için sesli işaret verdikten sonra eğer herhangi bir oyuncu topa dokunursa bu bir ihlaldir.\nÖrnek 31-8: A1'in son serbest atışından sonra top çemberden seker. Ribaund sırasında B2, A2'ye faul yapar. Bu B takımını...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Her iki durumda da bu A3 veya B3 tarafından yapılan topa müdahale ihlalidir. (a) Sayı verilmeyecektir. Her iki topu oyuna sokma hakkı cezası birbirini iptal edecektir. Oyun pozisyon sırasına göre doğrudan arkalığın arkası hariç dip çizginin gerisinde faulün olduğu en yakın yerden topun oyuna sokulmasıyla devam edecektir. (b) A1’e 1 sayı verilecektir. B2’nin faulünün bir sonucu olarak oyun A takımı tarafından doğrudan arkalığın arkası hariç kendi dip çizgisinin gerisinde faulün olduğu en yakın yerden topun oyuna sokulmasıyla devam edecektir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "Madde 31 Sayıya yönelen top ve müdahale | 31-7\nAçıklama: Aşağıdaki durumlarda top çembere temas ettikten sonra ve topun hala sepete girme olasılığı varken bir faul çalınır. • sayı amacıyla bir şut girişiminde, • başarısız bir son serbest atışta, • oyun saati çeyreğin ya da uzatmanın sonu için sesli işaret verdikten sonra eğer herhangi bir oyuncu topa dokunursa bu bir ihlaldir.\nÖrnek 31-9: A1'in son serbest atışından sonra top çemberden seker. Ribaund sırasında B2, A2'ye faul yapar. Bu B takımını...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Her iki durumda da bu A3 veya B3 tarafından yapılan bir müdahale ihlalidir. (a) Sayı verilmeyecektir. (b) A1’e 1 sayı verilecektir. Her iki durumda da B2'nin faulünün bir sonucu olarak A2, 2 serbest atış atacaktır. Oyun herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir.",
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': "Madde 31 Sayıya yönelen top ve müdahale | 31-7\nAçıklama: Aşağıdaki durumlarda top çembere temas ettikten sonra ve topun hala sepete girme olasılığı varken bir faul çalınır. • sayı amacıyla bir şut girişiminde, • başarısız bir son serbest atışta, • oyun saati çeyreğin ya da uzatmanın sonu için sesli işaret verdikten sonra eğer herhangi bir oyuncu topa dokunursa bu bir ihlaldir.\nÖrnek 31-10: A1'in son serbest atışından sonra top çemberden seker. Ribaund sırasında A2, B2'ye faul yapar. Bu, A takımı...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Her iki durumda da bu A3 veya B3 tarafından yapılan bir müdahale ihlalidir. (c) Sayı verilmeyecektir. (d) A1’e 1 sayı verilecektir. Her iki durumda da A2'nin faulünün bir sonucu olarak B2, 2 serbest atış kullanacaktır. Oyun herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir.",
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': "Madde 31 Sayıya yönelen top ve müdahale | 31-7\nAçıklama: Aşağıdaki durumlarda top çembere temas ettikten sonra ve topun hala sepete girme olasılığı varken bir faul çalınır. • sayı amacıyla bir şut girişiminde, • başarısız bir son serbest atışta, • oyun saati çeyreğin ya da uzatmanın sonu için sesli işaret verdikten sonra eğer herhangi bir oyuncu topa dokunursa bu bir ihlaldir.\nÖrnek 31-11: A1'in son serbest atışından sonra top çemberden seker. Ribaund sırasında B2 ve A2 arasında çift faul durumu...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Her iki durumda da bu A3 veya B3 tarafından yapılan bir müdahale ihlalidir. Faul maç kağıdında her yapanın kendisine yazılacaktır. (a) Sayı verilmeyecektir. Oyun doğrudan arkalığın arkası hariç dip çizginin gerisinde, çift faulün meydana geldiği en yakın yerden pozisyon sırasına göre topun oyuna sokulmasıyla devam edecektir. (b) A1’e 1 sayı verilecektir. Çift faul cezaları birbirini iptal edecektir. Oyun B takımı tarafından, dip çizgisinin gerisindeki herhangi bir yerden herhangi bir başarılı son serbest atıştan sonra olduğu gibi devam edecektir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-7\nAçıklama: Aşağıdaki durumlarda top çembere temas ettikten sonra ve topun hala sepete girme olasılığı varken bir faul çalınır. • sayı amacıyla bir şut girişiminde, • başarısız bir son serbest atışta, • oyun saati çeyreğin ya da uzatmanın sonu için sesli işaret verdikten sonra eğer herhangi bir oyuncu topa dokunursa bu bir ihlaldir.\nÖrnek 31-12: A1 sayı amacıyla bir şut girişiminde bulunur. Top çemberden seker ve hala sepete girme olasılığı varken oyu...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda bu bir topa müdahale ihlalidir. Oyun saati çeyreğin sonu için sesli işaret verdikten sonra hiçbir oyuncu çembere değen ve hala sepete girme olasılığı olan topa dokunamayacaktır. (a) A1’e sayı verilmeyecektir. (b) A1’e 2 ya da 3 sayı verilecektir. (c) Çeyrek sona ermiştir. (d) A1’e 2 ya da 3 sayı verilecektir. Tüm durumlarda üçüncü çeyrek sona ermiştir. Oyun orta çizgi uzantısından pozisyon sırasına göre topun oyuna sokulmasıyla devam edecektir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-13\nAçıklama: Eğer bir oyuncu, sayı amacıyla yapılan bir şut girişimi sırasında sepete doğru giden topa temas ederse tüm sayıya yönelen top ve müdahale kısıtlamaları uygulanacaktır.\nÖrnek 31-14: A1 2 sayılık atış girişiminde bulunur. Yükselmekte olan topa A2 ya da B2 tarafından temas edilir. Top sepete doğru inerken, (a) A3 topa temas eder. (b) B3 topa temas eder.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A2 ve B2’nin yükselmekte olan topa teması kurallara uygundur. Sadece A3 ya da B3’ün inmekte olan topa teması sayıya yönelen topa yapılan bir ihlaldir. (a) B takımına serbest atış çizgisinin uzantısından topu oyuna sokma hakkı verilecektir. (b) A1’e 2 sayı verilecektir.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-13\nAçıklama: Eğer bir oyuncu, sayı amacıyla yapılan bir şut girişimi sırasında sepete doğru giden topa temas ederse tüm sayıya yönelen top ve müdahale kısıtlamaları uygulanacaktır.\nÖrnek 31-15: A1 sayı amacıyla bir şut girişiminde bulunur. Top en yüksek seviyesine ulaştığında çember seviyesinin üzerindeyken A2 veya B2 tarafından temas edilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A2 veya B2’nin topa teması kurallara uygundur. Topa ancak en yüksek seviyesine ulaştıktan ve aşağı doğru inmeye başladıktan sonra dokunulursa kural dışı bir temas olarak kabul edilir.',
                'choices': [
                    ('A2 veya B2’nin topa teması kurallara uygundur. Topa ancak en yüksek seviyesine ulaştıktan ve aşağı doğru inmeye başladıktan sonra dokunulursa kural dışı bir te…', True),
                    ('A2 veya B2’nin topa teması kurallara uygun değildir. Topa ancak en yüksek seviyesine ulaştıktan ve aşağı doğru inmeye başladıktan sonra dokunulursa kural dışı bir te…', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-16\nAçıklama: Bir hakemin değerlendirmesine göre bir oyuncunun topun sepete girmesini engelleyecek ya da sepete girmesine neden olacak şekilde arkalığın ya da çemberin sallanmasına sebep olması bir müdahale ihlalidir.\nÖrnek 31-17: A1 oyunun sonuna doğru 3 sayılık bir atış girişiminde bulunur. Top havadayken oyun saati oyunun sonu için sesli işaret verir. Sesli işaretten sonra hakemin değerlendirmesine göre , (a) B1 arkalığın ya da çemberin sallanmasına...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyunun sonu için oyun saati sesli işaret verdikten sonra bile top canlı kalır. Bu bir müdahale ihlalidir ve, (a) B1’in ihlali sonucunda A1’e 3 sayı verilecektir. (b) A2’nin ihlali sonucunda sayı geçerli sayılmayacaktır.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-18\nAçıklama: Sayı amacıyla yapılan bir atış sırasında top çemberle temas halindeyken ve hala sepete girme olasılığı varken bir savunma ya da hücum oyuncusunun sepete (çember ya da fileye) veya arkalığa temas etmesi bir müdahale ihlalidir.\nDiyagram Diyagram 3: Çemberle temas halindeki top\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '',
                'choices': [
                    ('Açıklama: Sayı amacıyla yapılan bir atış sırasında top çemberle temas halindeyken ve hala sepete girme olasılığı varken bir savunma ya da hücum oyuncusunun sep…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-18\nAçıklama: Sayı amacıyla yapılan bir atış sırasında top çemberle temas halindeyken ve hala sepete girme olasılığı varken bir savunma ya da hücum oyuncusunun sepete (çember ya da fileye) veya arkalığa temas etmesi bir müdahale ihlalidir.\nÖrnek 31-19: A1’in sayı amacıyla attığı şut sonrasında top çembere çarpıp yükselir ve tekrar çembere doğru iner. Top çemberdeyken B1 sepete ya da arkalığa temas eder.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu B1 tarafından yapılan bir müdahale ihlalidir. Topun sepete girme olasılığı olduğu sürece müdahale kısıtlamaları geçerlidir.',
                'choices': [
                    ('Bu B1 tarafından yapılan bir müdahale ihlalidir. Topun sepete girme olasılığı olduğu sürece müdahale kısıtlamaları geçerlidir.', True),
                    ('Bu B1 tarafından yapılan bir müdahale ihlalidir. Topun sepete girme olasılığı olduğu sürece müdahale kısıtlamaları geçerli değildir.', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-18\nAçıklama: Sayı amacıyla yapılan bir atış sırasında top çemberle temas halindeyken ve hala sepete girme olasılığı varken bir savunma ya da hücum oyuncusunun sepete (çember ya da fileye) veya arkalığa temas etmesi bir müdahale ihlalidir.\nÖrnek 31-20: A1’in sayı amacıyla attığı şut tamamen çember seviyesinin üzerinde ve inmekteyken topa aynı anda A2 ve B2 tarafından temas edilir. Sonra top: (a) Sepete girer. (b) Sepete girmez.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A2 ve B2 tarafından sayıya yönelen topa yapılan bir ihlaldir. Her iki durumda da sayı verilmeyecektir. Bu bir hava atışı durumudur.',
                'choices': [
                    ('Bu A2 ve B2 tarafından sayıya yönelen topa yapılan bir ihlaldir. Her iki durumda da sayı verilmeyecektir. Bu bir hava atışı durumudur.', True),
                    ('Bu A2 ve B2 tarafından sayıya yönelen topa yapılan bir ihlaldir. Her iki durumda da sayı verilecektir. Bu bir hava atışı durumudur.', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-21\nAçıklama: Bir oyuncun topla oynamak için sepeti (çember ya da fileyi) tutması bir müdahale ihlalidir.\nÖrnek 31-22: A1 sayı amacıyla bir şut girişiminde bulunur. Top çemberden seker ve yükselir, sonrasında, (a) A2 çemberi tutar ve topu sepetin içine doğru tipler. (b) A2 topun hala sepete girme olasılığı varken çemberi tutar. Top sepete girer. (c) B2 çemberi tutar ve topu sepetin dışına tipler. (d) B2 topun hala sepete girme olasılığı varken çemberi ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her durumda da bu A2 ve B2 tarafından yapılan bir müdahale ihlalidir. (a) ve (b) Sayı verilmeyecektir. Oyun B takımının serbest atış çizgisi uzantısından topu oyuna sokmasıyla devam edecektir. (c) ve (d) A1’e 2 ya da 3 sayı verilecektir. Oyun B takımı tarafından herhangi bir başarılı atış sonrasında olduğu gibi dip çizgisinden topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-23\nAçıklama: Top sepetin içerisindeyken bir savunma oyuncusu topa temas ederse bu bir müdahale ihlalidir.\nDiyagram Diyagram 4: Sepetin içindeki top\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '',
                'choices': [
                    ('Açıklama: Top sepetin içerisindeyken bir savunma oyuncusu topa temas ederse bu bir müdahale ihlalidir. Sepetin içindeki top', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-23\nAçıklama: Top sepetin içerisindeyken bir savunma oyuncusu topa temas ederse bu bir müdahale ihlalidir.\nÖrnek 31-24: A1 sayı amacıyla 2 sayılık atış bölgesinden bir şut girişiminde bulunur. Topun çok az bir parçası sepetin içinde ve çemberin etrafında dönmekteyken, (a) B1 tarafından topa temas edilir. (b) A2 tarafından topa temas edilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Topun çok küçük bir parçası bile çember seviyesinin altında ve içindeyken top sepetin içindedir. (a) Bu B1 tarafından yapılan bir müdahale ihlalidir. A1'e 2 sayı verilecektir. (b) Bu A2'nin kurallara uygun bir müdahalesidir. Ancak hücum oyuncusu topa dokunabilir.",
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 31 Sayıya yönelen top ve müdahale | 31-23\nAçıklama: Top sepetin içerisindeyken bir savunma oyuncusu topa temas ederse bu bir müdahale ihlalidir.\nÖrnek 31-25: A1 sayı amacıyla 2 sayılık atış bölgesinden bir şut girişiminde bulunur. Topun çok az bir parçası sepetin içinde ve çemberin etrafında dönmekteyken oyun saati çeyreğin sonu için sesli işaretini verir. Oyun saatinin sesli işaretinden sonra; (a) A2 (b) B2 topa dokunur.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu durum bir topa müdahale ihlalidir. (a) A2. Atış başarılı olsa bile sayılmayacaktır. (b) B2. A1’e 2 sayı verilecektir. Çeyreğin sonu için oyun saati sesli işaret verdikten sonra topa her iki takımdan bir oyuncu tarafından dokunulduğunda top hemen ölür.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 33 Temas: Genel prensipler | 33-1\nAçıklama: Silindir prensibi savunma veya hücum oyuncusu olup olmadıklarına bakılmaksızın tüm oyuncular için geçerlidir.\nÖrnek 33-2: A1 sayı amacıyla 3 sayılık atış girişiminde havadadır. A1 bacağını uzatarak savunma oyuncusu olan B1’e bir temasta bulunur.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Bu durum, bacağını kendi silindirinin dışına çıkardığı ve savunma oyuncusu olan B1 ile temas ettiği için A1'in yaptığı bir fauldür.",
                'choices': [
                    ("Bu durum, bacağını kendi silindirinin dışına çıkardığı ve savunma oyuncusu olan B1 ile temas ettiği için A1'in yaptığı bir fauldür.", True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 33 Temas: Genel prensipler | 33-3\nAçıklama: Şarjsız yarım daire kuralının amacı topu kontrol eden ve sepete doğru yüklenen bir hücum oyuncusuna şarj faulü aldırmak için kendi sepeti altında pozisyon alan bir savunma oyuncusunu ödüllendirmemektir. (Madde 33.10) Şarjsız yarım daire kuralı şu durumlarda uygulanacaktır: (a) Savunma oyuncusu bir ya da iki ayağıyla yarım daire alanına temas edecektir (Diyagram 5). Yarım daire çizgisi, yarım daire alanının parçasıdır. (b) Hücum oyuncusu yarım dai...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '',
                'choices': [
                    ('Açıklama: Şarjsız yarım daire kuralının amacı topu kontrol eden ve sepete doğru yüklenen bir hücum oyuncusuna şarj faulü aldırmak için kendi sepeti altında poz…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 33 Temas: Genel prensipler | 33-3\nAçıklama: Şarjsız yarım daire kuralının amacı topu kontrol eden ve sepete doğru yüklenen bir hücum oyuncusuna şarj faulü aldırmak için kendi sepeti altında pozisyon alan bir savunma oyuncusunu ödüllendirmemektir. (Madde 33.10) Şarjsız yarım daire kuralı şu durumlarda uygulanacaktır: (a) Savunma oyuncusu bir ya da iki ayağıyla yarım daire alanına temas edecektir (Diyagram 5). Yarım daire çizgisi, yarım daire alanının parçasıdır. (b) Hücum oyuncusu yarım dai...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in hareketi kurallara uygundur. Şarjsız yarım daire kuralı uygulanacaktır.',
                'choices': [
                    ('A1’in hareketi kurallara uygundur. Şarjsız yarım daire kuralı uygulanacaktır.', True),
                    ('A1’in hareketi kurallara uygun değildir. Şarjsız yarım daire kuralı uygulanacaktır.', False),
                ]
            },
            {
                'text': 'Madde 33 Temas: Genel prensipler | 33-3\nAçıklama: Şarjsız yarım daire kuralının amacı topu kontrol eden ve sepete doğru yüklenen bir hücum oyuncusuna şarj faulü aldırmak için kendi sepeti altında pozisyon alan bir savunma oyuncusunu ödüllendirmemektir. (Madde 33.10) Şarjsız yarım daire kuralı şu durumlarda uygulanacaktır: (a) Savunma oyuncusu bir ya da iki ayağıyla yarım daire alanına temas edecektir (Diyagram 5). Yarım daire çizgisi, yarım daire alanının parçasıdır. (b) Hücum oyuncusu yarım dai...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A1’in takım kontrol faulüdür. Şarjsız yarım daire kuralı uygulanmayacaktır. A1 şarjsız yarım daire alanına sahanın doğrudan arkalığın arkasından ve uzatılmış hayali çizgisinden girmiştir.',
                'choices': [
                    ('Bu A1’in takım kontrol faulüdür. Şarjsız yarım daire kuralı uygulanmayacaktır. A1 şarjsız yarım daire alanına sahanın doğrudan arkalığın arkasından ve uzatılmı…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 33 Temas: Genel prensipler | 33-3\nAçıklama: Şarjsız yarım daire kuralının amacı topu kontrol eden ve sepete doğru yüklenen bir hücum oyuncusuna şarj faulü aldırmak için kendi sepeti altında pozisyon alan bir savunma oyuncusunu ödüllendirmemektir. (Madde 33.10) Şarjsız yarım daire kuralı şu durumlarda uygulanacaktır: (a) Savunma oyuncusu bir ya da iki ayağıyla yarım daire alanına temas edecektir (Diyagram 5). Yarım daire çizgisi, yarım daire alanının parçasıdır. (b) Hücum oyuncusu yarım dai...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A2’nin takım kontrol faulüdür. Şarjsız yarım daire kuralı uygulanmayacaktır.',
                'choices': [
                    ('Bu A2’nin takım kontrol faulüdür. Şarjsız yarım daire kuralı uygulanmayacaktır.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 33 Temas: Genel prensipler | 33-3\nAçıklama: Şarjsız yarım daire kuralının amacı topu kontrol eden ve sepete doğru yüklenen bir hücum oyuncusuna şarj faulü aldırmak için kendi sepeti altında pozisyon alan bir savunma oyuncusunu ödüllendirmemektir. (Madde 33.10) Şarjsız yarım daire kuralı şu durumlarda uygulanacaktır: (a) Savunma oyuncusu bir ya da iki ayağıyla yarım daire alanına temas edecektir (Diyagram 5). Yarım daire çizgisi, yarım daire alanının parçasıdır. (b) Hücum oyuncusu yarım dai...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A1’in takım kontrol faulüdür. Şarjsız yarım daire kuralı uygulanmayacaktır. A1, A2’nin sepete doğru giden yolunu açmak için vücudunu kural dışı olarak kullanmıştır.',
                'choices': [
                    ('Bu A1’in takım kontrol faulüdür. Şarjsız yarım daire kuralı uygulanmayacaktır. A1, A2’nin sepete doğru giden yolunu açmak için vücudunu kural dışı olarak kulla…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 33 Temas: Genel prensipler | 33-3\nAçıklama: Şarjsız yarım daire kuralının amacı topu kontrol eden ve sepete doğru yüklenen bir hücum oyuncusuna şarj faulü aldırmak için kendi sepeti altında pozisyon alan bir savunma oyuncusunu ödüllendirmemektir. (Madde 33.10) Şarjsız yarım daire kuralı şu durumlarda uygulanacaktır: (a) Savunma oyuncusu bir ya da iki ayağıyla yarım daire alanına temas edecektir (Diyagram 5). Yarım daire çizgisi, yarım daire alanının parçasıdır. (b) Hücum oyuncusu yarım dai...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in hareketi kurallara uygundur. Şarjsız yarım daire kuralı uygulanacaktır.',
                'choices': [
                    ('A1’in hareketi kurallara uygundur. Şarjsız yarım daire kuralı uygulanacaktır.', True),
                    ('A1’in hareketi kurallara uygun değildir. Şarjsız yarım daire kuralı uygulanacaktır.', False),
                ]
            },
            {
                'text': 'Madde 33 Temas: Genel prensipler | 33-3\nAçıklama: Şarjsız yarım daire kuralının amacı topu kontrol eden ve sepete doğru yüklenen bir hücum oyuncusuna şarj faulü aldırmak için kendi sepeti altında pozisyon alan bir savunma oyuncusunu ödüllendirmemektir. (Madde 33.10) Şarjsız yarım daire kuralı şu durumlarda uygulanacaktır: (a) Savunma oyuncusu bir ya da iki ayağıyla yarım daire alanına temas edecektir (Diyagram 5). Yarım daire çizgisi, yarım daire alanının parçasıdır. (b) Hücum oyuncusu yarım dai...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bu A1’in takım kontrol faulüdür. A1 kolunu kural dışı olarak kullandığından dolayı şarjsız yarım daire kuralı uygulanmayacaktır.',
                'choices': [
                    ('Bu A1’in takım kontrol faulüdür. A1 kolunu kural dışı olarak kullandığından dolayı şarjsız yarım daire kuralı uygulanmayacaktır.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 33 Temas: Genel prensipler | 33-3\nAçıklama: Şarjsız yarım daire kuralının amacı topu kontrol eden ve sepete doğru yüklenen bir hücum oyuncusuna şarj faulü aldırmak için kendi sepeti altında pozisyon alan bir savunma oyuncusunu ödüllendirmemektir. (Madde 33.10) Şarjsız yarım daire kuralı şu durumlarda uygulanacaktır: (a) Savunma oyuncusu bir ya da iki ayağıyla yarım daire alanına temas edecektir (Diyagram 5). Yarım daire çizgisi, yarım daire alanının parçasıdır. (b) Hücum oyuncusu yarım dai...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "B1’in hareketi kurallara uygundur. Şarjsız yarım daire kuralı, B1'in yarım daire alanına temas eden bir veya her iki ayağı olmadığı için uygulanmayacaktır. Olası herhangi bir temas kurallara göre değerlendirilecektir.",
                'choices': [
                    ("B1’in hareketi kurallara uygundur. Şarjsız yarım daire kuralı, B1'in yarım daire alanına temas eden bir veya her iki ayağı olmadığı için uygulanmayacaktır. Ola…", True),
                    ("B1’in hareketi kurallara uygun değildir. Şarjsız yarım daire kuralı, B1'in yarım daire alanına temas eden bir veya her iki ayağı olmadığı için uygulanmayacaktır. Ola…", False),
                ]
            },
            {
                'text': "Madde 33 Temas: Genel prensipler | 33-11\nAçıklama: Kişisel bir faul, bir oyuncunun rakibine kural dışı temasıdır. Rakibine karşı kural dışı temasa neden olan oyuncu buna göre cezalandırılacaktır.\nÖrnek 33-12: A1 sayı amacıyla bir şut girişiminde bulunur. B1 takım arkadaşı B2'yi iterek daha sonra atış halinde olan A1’e kural dışı bir temasa sebebiyet verir. Top sepetten içeri girer.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'A1’e 2 ya da 3 sayı verilecektir. B2, A1’e temas etmiştir ve bir faulle cezalandırılacaktır. A1, 1 serbest atış kullanacaktır. Oyun herhangi bir son serbest atıştan sonra olduğu gibi devam edecektir.',
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': "Madde 33 Temas: Genel prensipler | 33-11\nAçıklama: Kişisel bir faul, bir oyuncunun rakibine kural dışı temasıdır. Rakibine karşı kural dışı temasa neden olan oyuncu buna göre cezalandırılacaktır.\nÖrnek 33-13: A1 sayı amacıyla bir şut girişiminde bulunur. B1, A2'yi iter ve bu durum takım arkadaşı olan A1’e kural dışı bir temasa sebebiyet verir. Bu B takımının o çeyrekteki üçüncü takım faulüdür.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "A1’e 2 ya da 3 sayı verilecektir. A takımına B2'nin yaptığı faulün meydana geldiği en yakın yerden topu oyuna sokma hakkı verilecektir.",
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 34 Kişisel faul | 34-1\nAçıklama: Oyun saati dördüncü çeyrekte veya her uzatmada 2:00 veya daha az gösterdiğinde ve top hakemin elinde ya da topu oyuna sokacak olan oyuncunun kullanımındadır. Eğer bu sırada bir savunma oyuncusu sahadaki bir hücum oyuncusuna kural dışı bir şekilde temas ederse, temas sportmenlik dışı faul kriterlerini karşılamadığı sürece bu bir topun oyuna sokulması faulüdür. Faul yapılan oyuncu, dördüncü çeyrekteki takım faullerinin sayısına bakılmaksızın kimse dizilmeden ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B takımının dördüncü çeyrekteki faul sayısına bakılmaksızın A2 kimse dizilmeden 1 serbest atış kullanacaktır. Oyun A takımı tarafından B2’nin yaptığı faulünün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. Eğer yapılan faul, (a) A takımının geri sahasındaysa şut saatinde 24 saniyesi olacaktır. (b) A takımının ön sahasındaysa ve eğer şut saati14 saniye veya daha fazla gösteriyorsa kalan süresi, eğer şut saati 13 saniye veya daha az gösteriliyorsa 14 saniyesi olacaktır.',
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 34 Kişisel faul | 34-1\nAçıklama: Oyun saati dördüncü çeyrekte veya her uzatmada 2:00 veya daha az gösterdiğinde ve top hakemin elinde ya da topu oyuna sokacak olan oyuncunun kullanımındadır. Eğer bu sırada bir savunma oyuncusu sahadaki bir hücum oyuncusuna kural dışı bir şekilde temas ederse, temas sportmenlik dışı faul kriterlerini karşılamadığı sürece bu bir topun oyuna sokulması faulüdür. Faul yapılan oyuncu, dördüncü çeyrekteki takım faullerinin sayısına bakılmaksızın kimse dizilmeden ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "B2'nin A2'ye yaptığı temas sportmenlik dışı faul kriterlerini karşılamıyorsa, bu bir topun oyuna sokulması faulüdür. B takımının dördüncü çeyrekteki faul sayısına bakılmaksızın A2 kimse dizilmeden 1 serbest atış kullanacaktır. Oyun A takımı tarafından arkalığın doğrudan arkası hariç B2’nin yaptığı faulünün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. Eğer topun oyuna sokulması dip çizgiden yönetilecekse A takımının topu oyuna sokacak olan oyuncusunun topu ellerinden çıkarmadan önce başarılı bir sayı veya son serbest atıştan sonra olduğu gibi belirlenmiş yer haricinde kurallara aykırı olarak hareket etme veya dip çizginin gerisindeki bir takım arkadaşına pas verme hakkı olmayacaktır.",
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 34 Kişisel faul | 34-1\nAçıklama: Oyun saati dördüncü çeyrekte veya her uzatmada 2:00 veya daha az gösterdiğinde ve top hakemin elinde ya da topu oyuna sokacak olan oyuncunun kullanımındadır. Eğer bu sırada bir savunma oyuncusu sahadaki bir hücum oyuncusuna kural dışı bir şekilde temas ederse, temas sportmenlik dışı faul kriterlerini karşılamadığı sürece bu bir topun oyuna sokulması faulüdür. Faul yapılan oyuncu, dördüncü çeyrekteki takım faullerinin sayısına bakılmaksızın kimse dizilmeden ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "B2'nin A2'ye yaptığı temas sportmenlik dışı faul kriterlerini karşılamıyorsa bu bir topun oyuna sokulması faulüdür. A2'ye kimse dizilmeden 1 serbest atış hakkı verilecektir. Oyun A takımı tarafından B2’nin yaptığı faulünün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 34 Kişisel faul | 34-1\nAçıklama: Oyun saati dördüncü çeyrekte veya her uzatmada 2:00 veya daha az gösterdiğinde ve top hakemin elinde ya da topu oyuna sokacak olan oyuncunun kullanımındadır. Eğer bu sırada bir savunma oyuncusu sahadaki bir hücum oyuncusuna kural dışı bir şekilde temas ederse, temas sportmenlik dışı faul kriterlerini karşılamadığı sürece bu bir topun oyuna sokulması faulüdür. Faul yapılan oyuncu, dördüncü çeyrekteki takım faullerinin sayısına bakılmaksızın kimse dizilmeden ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A2 kimse dizilmeden 2 serbest atış kullanacaktır. Oyun A takımı tarafından kendi ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 34 Kişisel faul | 34-1\nAçıklama: Oyun saati dördüncü çeyrekte veya her uzatmada 2:00 veya daha az gösterdiğinde ve top hakemin elinde ya da topu oyuna sokacak olan oyuncunun kullanımındadır. Eğer bu sırada bir savunma oyuncusu sahadaki bir hücum oyuncusuna kural dışı bir şekilde temas ederse, temas sportmenlik dışı faul kriterlerini karşılamadığı sürece bu bir topun oyuna sokulması faulüdür. Faul yapılan oyuncu, dördüncü çeyrekteki takım faullerinin sayısına bakılmaksızın kimse dizilmeden ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Oyun, herhangi bir B takımı oyuncusunun kullanacağı 1 serbest atışın ardından A2 tarafından kullanılacak 1 serbest atış ve B2'nin yaptığı faulden dolayı A takımının faulünün yapıldığı en yakın yerden topu oyuna sokmasıyla devam edecektir. Topun oyuna sokulması geri sahadan ise A takımının şut saatinde 24 saniyesi olacaktır. Ön sahadan ise şut saati 13 saniye veya daha az gösteriyorsa A takımının şut saatinde 14 saniyesi olacaktır, şut saati 14 saniye veya daha fazla süre gösteriyorsa kalan süre kadar zamanı olacaktır.",
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 34 Kişisel faul | 34-1\nAçıklama: Oyun saati dördüncü çeyrekte veya her uzatmada 2:00 veya daha az gösterdiğinde ve top hakemin elinde ya da topu oyuna sokacak olan oyuncunun kullanımındadır. Eğer bu sırada bir savunma oyuncusu sahadaki bir hücum oyuncusuna kural dışı bir şekilde temas ederse, temas sportmenlik dışı faul kriterlerini karşılamadığı sürece bu bir topun oyuna sokulması faulüdür. Faul yapılan oyuncu, dördüncü çeyrekteki takım faullerinin sayısına bakılmaksızın kimse dizilmeden ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A takımı A2'nin takım kontrol faulünden bir avantaj elde etmemiştir. Sportmenlik dışı veya diskalifiye edici faul kriterlerini karşılayan bir temas olmadıkça A2'ye bir kişisel faul verilecektir. Oyun B takımı tarafından A2’nin yaptığı faulünün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 34 Kişisel faul | 34-1\nAçıklama: Oyun saati dördüncü çeyrekte veya her uzatmada 2:00 veya daha az gösterdiğinde ve top hakemin elinde ya da topu oyuna sokacak olan oyuncunun kullanımındadır. Eğer bu sırada bir savunma oyuncusu sahadaki bir hücum oyuncusuna kural dışı bir şekilde temas ederse, temas sportmenlik dışı faul kriterlerini karşılamadığı sürece bu bir topun oyuna sokulması faulüdür. Faul yapılan oyuncu, dördüncü çeyrekteki takım faullerinin sayısına bakılmaksızın kimse dizilmeden ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "B2'nin A2'ye yaptığı temas sportmenlik dışı faul kriterlerini karşılamıyorsa bu bir topu oyuna sokma faulüdür. A2'ye kimse dizilmeden 1 serbest atış hakkı verilecektir. Oyun A takımı tarafından B2’nin yaptığı faulünün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 34 Kişisel faul | 34-1\nAçıklama: Oyun saati dördüncü çeyrekte veya her uzatmada 2:00 veya daha az gösterdiğinde ve top hakemin elinde ya da topu oyuna sokacak olan oyuncunun kullanımındadır. Eğer bu sırada bir savunma oyuncusu sahadaki bir hücum oyuncusuna kural dışı bir şekilde temas ederse, temas sportmenlik dışı faul kriterlerini karşılamadığı sürece bu bir topun oyuna sokulması faulüdür. Faul yapılan oyuncu, dördüncü çeyrekteki takım faullerinin sayısına bakılmaksızın kimse dizilmeden ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Top, topu oyuna sokmakta olan A1'in ellerini zaten terk ettiğinden dolayı bu bir topun oyuna sokulması faulü değildir. B2'nin A2'ye teması sportmenlik dışı veya diskalifiye edici faul kriterlerini karşılamıyorsa bu bir kişisel fauldür ve buna göre cezalandırılacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 35 Çift faul | 35-1\nAçıklama: Bir faul kişisel, sportmenlik dışı, diskalifiye edici veya teknik faul olabilir. Çift faul olarak kabul edilebilmesi için her iki faulün de aynı 2 rakip arasındaki oyuncunun faulü olmalı ve aynı kategoride olmalıdır, her ikisi de kişisel faul veya her ikisi de sportmenlik dışı ve diskalifiye edici faullerin herhangi bir kombinasyonudur. Takımların, takım faullerine bakılmaksızın serbest atış verilmeyecektir. Çift faul fiziksel temas içermelidir, bu nedenle tek...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Teknik fauller çift faulün parçası değildir. Cezalar birbirini iptal edecektir. Oyun ilk teknik faul gerçekleştiğinde topun bulunduğu en yakın yerden A takımının topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde kalan süresi kadar zamanı olacaktır.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 35 Çift faul | 35-1\nAçıklama: Bir faul kişisel, sportmenlik dışı, diskalifiye edici veya teknik faul olabilir. Çift faul olarak kabul edilebilmesi için her iki faulün de aynı 2 rakip arasındaki oyuncunun faulü olmalı ve aynı kategoride olmalıdır, her ikisi de kişisel faul veya her ikisi de sportmenlik dışı ve diskalifiye edici faullerin herhangi bir kombinasyonudur. Takımların, takım faullerine bakılmaksızın serbest atış verilmeyecektir. Çift faul fiziksel temas içermelidir, bu nedenle tek...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki faul de aynı kategoridedir (kişisel fauller), bundan dolayı bu bir çift fauldür. Çeyrekte farklı sayıda olan takım faulleri dikkate alınmaz. Oyun A takımı tarafından çift faulün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde kalan süresi kadar zamanı olacaktır.',
                'choices': [
                    ('Kişisel faul', True),
                    ('Faul yok / oyun devam', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 35 Çift faul | 35-1\nAçıklama: Bir faul kişisel, sportmenlik dışı, diskalifiye edici veya teknik faul olabilir. Çift faul olarak kabul edilebilmesi için her iki faulün de aynı 2 rakip arasındaki oyuncunun faulü olmalı ve aynı kategoride olmalıdır, her ikisi de kişisel faul veya her ikisi de sportmenlik dışı ve diskalifiye edici faullerin herhangi bir kombinasyonudur. Takımların, takım faullerine bakılmaksızın serbest atış verilmeyecektir. Çift faul fiziksel temas içermelidir, bu nedenle tek...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Her iki faul de aynı kategoridedir (kişisel fauller), bundan dolayı bu bir çift fauldür. Eğer A1'in şutu başarılı olursa sayı geçerli sayılmayacaktır. Oyun A takımı tarafından serbest atış çizgisinin uzantısından topu oyuna sokmasıyla devam edecektir. Eğer A1'in atışı başarısız olursa oyun A takımı tarafından çift faulün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde kalan süresi kadar zamanı olacaktır.",
                'choices': [
                    ('Kişisel faul', True),
                    ('Faul yok / oyun devam', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 35 Çift faul | 35-1\nAçıklama: Bir faul kişisel, sportmenlik dışı, diskalifiye edici veya teknik faul olabilir. Çift faul olarak kabul edilebilmesi için her iki faulün de aynı 2 rakip arasındaki oyuncunun faulü olmalı ve aynı kategoride olmalıdır, her ikisi de kişisel faul veya her ikisi de sportmenlik dışı ve diskalifiye edici faullerin herhangi bir kombinasyonudur. Takımların, takım faullerine bakılmaksızın serbest atış verilmeyecektir. Çift faul fiziksel temas içermelidir, bu nedenle tek...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Her iki faul de aynı kategoridedir (kişisel fauller), bundan dolayı bu bir çift fauldür. Eğer A1'in şutu başarılı olursa sayı geçerli sayılacaktır. Oyun B takımı tarafından herhangi bir başarılı atış sonrasında olduğu gibi kendi dip çizgisinin gerisinden topu oyuna sokmasıyla devam edecektir. Eğer A1'in şutu başarılı olmazsa bu bir hava atışı durumudur. Oyun pozisyon sırasına göre topun oyuna sokulmasıyla devam edecektir.",
                'choices': [
                    ('Kişisel faul', True),
                    ('Faul yok / oyun devam', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 35 Çift faul | 35-1\nAçıklama: Bir faul kişisel, sportmenlik dışı, diskalifiye edici veya teknik faul olabilir. Çift faul olarak kabul edilebilmesi için her iki faulün de aynı 2 rakip arasındaki oyuncunun faulü olmalı ve aynı kategoride olmalıdır, her ikisi de kişisel faul veya her ikisi de sportmenlik dışı ve diskalifiye edici faullerin herhangi bir kombinasyonudur. Takımların, takım faullerine bakılmaksızın serbest atış verilmeyecektir. Çift faul fiziksel temas içermelidir, bu nedenle tek...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda bu bir çift fauldür. Oyun şu şekilde devam edecektir. (a) ve (c) Çift faulün meydana geldiği en yakın yerden A takımının topu oyuna sokmasıyla. (b) Pozisyon sırasına göre topun oyuna sokulmasıyla.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 35 Çift faul | 35-1\nAçıklama: Bir faul kişisel, sportmenlik dışı, diskalifiye edici veya teknik faul olabilir. Çift faul olarak kabul edilebilmesi için her iki faulün de aynı 2 rakip arasındaki oyuncunun faulü olmalı ve aynı kategoride olmalıdır, her ikisi de kişisel faul veya her ikisi de sportmenlik dışı ve diskalifiye edici faullerin herhangi bir kombinasyonudur. Takımların, takım faullerine bakılmaksızın serbest atış verilmeyecektir. Çift faul fiziksel temas içermelidir, bu nedenle tek...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'İki faul aynı kategoride değildir (kişisel ve sportmenlik dışı), bu nedenle bu bir çift faul değildir. Cezalar birbirini götürmez. A takımının topu oyuna sokma hakkı yönetilecek başka bir faul cezası olduğundan iptal edilecektir. B1 kimse dizilmeden 2 serbest atış kullanacaktır. Oyun B takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 35 Çift faul | 35-1\nAçıklama: Bir faul kişisel, sportmenlik dışı, diskalifiye edici veya teknik faul olabilir. Çift faul olarak kabul edilebilmesi için her iki faulün de aynı 2 rakip arasındaki oyuncunun faulü olmalı ve aynı kategoride olmalıdır, her ikisi de kişisel faul veya her ikisi de sportmenlik dışı ve diskalifiye edici faullerin herhangi bir kombinasyonudur. Takımların, takım faullerine bakılmaksızın serbest atış verilmeyecektir. Çift faul fiziksel temas içermelidir, bu nedenle tek...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'İki faul aynı kategoride değildir (kişisel ve sportmenlik dışı), bu nedenle bu bir çift faul değildir. Cezalar birbirini götürmez. Kişisel faul her zaman önce yapılmış olarak kabul edilecektir. A1 kimse dizilmeden 2 serbest atış kullanacaktır. B1 kimse dizilmeden 2 serbest atış kullanacaktır. Oyun B takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniye olacaktır.',
                'choices': [
                    ('Kişisel faul', True),
                    ('Faul yok / oyun devam', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 35 Çift faul | 35-1\nAçıklama: Bir faul kişisel, sportmenlik dışı, diskalifiye edici veya teknik faul olabilir. Çift faul olarak kabul edilebilmesi için her iki faulün de aynı 2 rakip arasındaki oyuncunun faulü olmalı ve aynı kategoride olmalıdır, her ikisi de kişisel faul veya her ikisi de sportmenlik dışı ve diskalifiye edici faullerin herhangi bir kombinasyonudur. Takımların, takım faullerine bakılmaksızın serbest atış verilmeyecektir. Çift faul fiziksel temas içermelidir, bu nedenle tek...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'İki faul aynı kategoride değildir (kişisel ve sportmenlik dışı), bu nedenle çift faul değildir. Cezalar birbirini götürmez. Kişisel faul her zaman önce yapılmış olarak kabul edilecektir. B takımının topu oyuna sokma cezası, yönetilecek başka bir faul cezası olduğundan iptal edilecektir. A1 kimse dizilmeden 2 serbest atış atacaktır. Oyun A takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniye olacaktır.',
                'choices': [
                    ('Kişisel faul', True),
                    ('Faul yok / oyun devam', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 35 Çift faul | 35-1\nAçıklama: Bir faul kişisel, sportmenlik dışı, diskalifiye edici veya teknik faul olabilir. Çift faul olarak kabul edilebilmesi için her iki faulün de aynı 2 rakip arasındaki oyuncunun faulü olmalı ve aynı kategoride olmalıdır, her ikisi de kişisel faul veya her ikisi de sportmenlik dışı ve diskalifiye edici faullerin herhangi bir kombinasyonudur. Takımların, takım faullerine bakılmaksızın serbest atış verilmeyecektir. Çift faul fiziksel temas içermelidir, bu nedenle tek...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda iki faul de aynı kategoridedir (kişisel/sportmenlik dışı/diskalifiye edici fauller), bundan dolayı bu bir çift fauldür. Oyun A takımı tarafından çift faulün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde kalan süresi kadar zamanı olacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-1\nAçıklama: Bir oyuncuya tekrarlanması halinde bir teknik faulle sonuçlanabilecek hareketinden ya da davranışından dolayı resmi bir uyarı verilir. Bu uyarı aynı zamanda o takımın başantrenörüne de bildirilecek ve o takımın herhangi bir üyesi için oyunun geri kalan zamanında benzer hareketler için de geçerli olacaktır. Bir resmi uyarı sadece top ölü olduğunda ve oyun saati durduğunda verilecektir.\nÖrnek 36-2: A1’e topun oyuna sokulmasına müdahale ettiği ya da tekrarlanma...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in uyarısı aynı zamanda A takımının başantrenörüne de bildirilecek ve oyunun geri kalan zamanında benzer hareketler için tüm A takımının üyeleri için geçerli olacaktır.',
                'choices': [
                    ('A1’in uyarısı aynı zamanda A takımının başantrenörüne de bildirilecek ve oyunun geri kalan zamanında benzer hareketler için tüm A takımının üyeleri için geçerl…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-3\nAçıklama: Bir oyuncu atış halindeyken rakiplerin el ya da ellerini atış yapan oyuncunun gözlerinin yakınına yaklaştırarak, yüksek sesle bağırarak, ayaklarını sert bir şekilde yere vurarak ya da atış yapan oyuncunun yakınında ellerini çırparak oyuncuyu rahatsız etmesine/şaşırtmasına izin verilmeyecektir. Atış yapan oyuncu bu hareketlerden dolayı dezavantajlı duruma düşerse bunların yapılması teknik faulle sonuçlanabilir ya da dezavantajlı duruma düşmezse uyarı verilebi...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "(a) A1’in sayısı geçerli sayılacaktır. B1’e bir uyarı verilecek ve bu uyarı aynı zamanda B takımı başantrenörüne de bildirilecektir. Oyun B takımı tarafından kendi dip çizgisinin gerisinden topu oyuna sokmasıyla devam edecektir. Eğer herhangi bir B takımı üyesine benzer bir davranış için daha önce bir uyarı verilmişse, B1’e bir teknik faul verilecektir. Herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. (b) B1'e bir teknik faul verilecektir. Herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun A takımı tarafından B1’e verilen teknik faulün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': "Madde 36 Teknik faul | 36-5\nAçıklama: Hakemler oyun saati çalışırken aynı takımdan 5'ten fazla oyuncunun aynı anda sahada olduğunu fark ederse en az 1 oyuncu kurallara aykırı olarak sahada kalmış veya tekrar yeniden sahaya girmiştir. Hata rakipleri dezavantajlı duruma düşürmeden mümkün olan en kısa zamanda düzeltilmelidir. Kurallara aykırı olarak katılımın fark edildiği anla oynanan süre ara geçen zaman arasında bütün olanlar geçerliliğini koruyacaktır. En az 1 oyuncu oyundan çıkarılacak ve o ta...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'B takımı dezavantajlı duruma düşmediği sürece oyun hemen durdurulacaktır. Baş antrenörün belirttiği bir A takımı oyuncusu oyundan çıkarılacaktır. A takımı başantrenörüne ‘B1 ’ olarak kaydedilen bir teknik faul verilecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': "Madde 36 Teknik faul | 36-5\nAçıklama: Hakemler oyun saati çalışırken aynı takımdan 5'ten fazla oyuncunun aynı anda sahada olduğunu fark ederse en az 1 oyuncu kurallara aykırı olarak sahada kalmış veya tekrar yeniden sahaya girmiştir. Hata rakipleri dezavantajlı duruma düşürmeden mümkün olan en kısa zamanda düzeltilmelidir. Kurallara aykırı olarak katılımın fark edildiği anla oynanan süre ara geçen zaman arasında bütün olanlar geçerliliğini koruyacaktır. En az 1 oyuncu oyundan çıkarılacak ve o ta...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Tüm durumlarda A takımı başantrenörüne ‘B1 ’ olarak kaydedilen bir teknik faul verilecektir. (a) A1’in faulü bir oyuncu faulüdür. (b) A1’in sayısı geçerli sayılacaktır. (c) A1, 2 ya da 3 serbest atış kullanacaktır. (d) A takımının altıncı oyuncusu oyun alanını terk eder. (a), (b) ve (c) Baş antrenörün belirttiği bir A takımı oyuncusu oyundan çıkarılacaktır.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-8\nAçıklama: Bir oyuncu kişisel, teknik veya sportmenlik dışı faul yaparak beşinci faulünü almasıyla oyun dışı kalmış bir oyuncu olur ve takım sıra bölgesinde oturabilir. Hakemler oyun saati çalışırken oyun dışı kalmış bir oyuncunun sahada olduğunu fark ederse o oyuncu kurallara aykırı bir şekilde sahada kalmış veya tekrar girmiş olmalıdır. Hata rakipleri dezavantajlı duruma düşürmeden derhal düzeltilmelidir. Kurallara aykırı olarak katılımın fark edildiği anla oynanan s...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A takımı dezavantajlı duruma düşmediği sürece oyun hemen durdurulacaktır. B1 oyundan çıkarılacaktır. B takımı başantrenörüne ‘B1 ’ olarak kaydedilen bir teknik faul verilecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-8\nAçıklama: Bir oyuncu kişisel, teknik veya sportmenlik dışı faul yaparak beşinci faulünü almasıyla oyun dışı kalmış bir oyuncu olur ve takım sıra bölgesinde oturabilir. Hakemler oyun saati çalışırken oyun dışı kalmış bir oyuncunun sahada olduğunu fark ederse o oyuncu kurallara aykırı bir şekilde sahada kalmış veya tekrar girmiş olmalıdır. Hata rakipleri dezavantajlı duruma düşürmeden derhal düzeltilmelidir. Kurallara aykırı olarak katılımın fark edildiği anla oynanan s...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun hemen durdurulacaktır. A1 oyundan çıkarılacaktır. A takımı başantrenörüne ‘B1 ’ olarak kaydedilen bir teknik faul verilecektir. (a) A1’in sayısı geçerli sayılacaktır. (b) A1’in faulü bir oyuncu faulüdür. Maç kağıdında beşinci faulünden sonraki boşluğa yazılacaktır. (c) A1’in yerine giren oyuncu 2 serbest atış kullanacaktır.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-8\nAçıklama: Bir oyuncu kişisel, teknik veya sportmenlik dışı faul yaparak beşinci faulünü almasıyla oyun dışı kalmış bir oyuncu olur ve takım sıra bölgesinde oturabilir. Hakemler oyun saati çalışırken oyun dışı kalmış bir oyuncunun sahada olduğunu fark ederse o oyuncu kurallara aykırı bir şekilde sahada kalmış veya tekrar girmiş olmalıdır. Hata rakipleri dezavantajlı duruma düşürmeden derhal düzeltilmelidir. Kurallara aykırı olarak katılımın fark edildiği anla oynanan s...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in sayısı geçerli sayılacaktır. A takımı başantrenörüne ‘B1 ’ olarak kaydedilen bir teknik faul verilecektir. Herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun B takımı tarafından oyun saatinde 1 saniye kala kendi dip çizginin gerisinden topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-12\nAçıklama: Bir oyuncu faul aldatması yaptığında aşağıdaki prosedür uygulanacaktır: • Hakem oyun durdurmadan “kolunun alt kısmını kaldırma” işaretini iki kez yaparak aldatmayı işaret edecektir. • Oyun durur durmaz hakem, o oyuncuya ve o takımın başantrenörüne uyarıyı bildirecektir. Her iki takımın da 1 uyarı hakkı vardır. • Bu takımdan herhangi bir oyuncu daha sonra bir faul aldatması yaptığında bir teknik faul verilecektir. Bu aynı zamanda oyun, o takımın herhangi bir...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Hakem “kolunun alt kısmını kaldırma” işaretini iki kez yaparak, başıyla yaptığı ilk aldatması için A1’e bir uyarı verir. Birinci aldatma için uyarıyı A1’e ya da A takım başantrenörüne bildirmek üzere oyun durmamış olsa bile, oyun sahası zeminine düşerek ikinci kez aldatma yapmasından dolayı A1 bir teknik faulle cezalandırılacaktır. (b) Hakem hem A1’e ve hem de B2’ye, “kolunun alt kısmını kaldırma” işaretini iki kez yaparak aldatmaları için birinci uyarıyı verir. Oyun saati ilk durduğu sırada uyarılar A1’e, B2’ye ve her iki takımın da başantrenörlerine bildirilecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-12\nAçıklama: Bir oyuncu faul aldatması yaptığında aşağıdaki prosedür uygulanacaktır: • Hakem oyun durdurmadan “kolunun alt kısmını kaldırma” işaretini iki kez yaparak aldatmayı işaret edecektir. • Oyun durur durmaz hakem, o oyuncuya ve o takımın başantrenörüne uyarıyı bildirecektir. Her iki takımın da 1 uyarı hakkı vardır. • Bu takımdan herhangi bir oyuncu daha sonra bir faul aldatması yaptığında bir teknik faul verilecektir. Bu aynı zamanda oyun, o takımın herhangi bir...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Hakem, “kolunun alt kısmını kaldırma” işaretini iki kez yaparak faul aldatması yaptığı için B1'e bir uyarı verecektir. Oyun saati durduğunda resmi uyarı kendi başantrenörüne de bildirilecek ve aynı zamanda takımının herhangi bir üyesi için de geçerli olacaktır.",
                'choices': [
                    ("Hakem, “kolunun alt kısmını kaldırma” işaretini iki kez yaparak faul aldatması yaptığı için B1'e bir uyarı verecektir. Oyun saati durduğunda resmi uyarı kendi …", True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-15\nAçıklama: Özellikle ribaund alınan ve yakından savunulan oyuncu durumlarında dirseklerin aşırı olarak sallanması ciddi yaralanmalara neden olabilir. Bu tür hareketler temasla sonuçlanırsa bir kişisel, sportmenlik dışı ya da diskalifiye edici faul çalınabilir. Eğer hareketler temasla sonuçlanmazsa bir teknik faul çalınabilir.\nÖrnek 36-16: A1 ribaund sırasında topu alır ve hemen B1 tarafından yakından savunulur. A1, B1’e temas etmeden pivot hareketi yapmak, pas vermek ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in hareketi kuralların ruhuna ve amacına uymamaktadır. A1’e bir teknik faul verilebilir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-17\nAçıklama: Bir oyuncuya 2 teknik faul verildiğinde diskalifiye edilecektir.\nÖrnek 36-18: A1’e birinci devre çembere asıldığı için ilk teknik faulü verilir. İkinci devrede A1, sportmenlik dışı davranışından dolayı ikinci bir teknik faulle cezalandırılır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A1 otomatik olarak diskalifiye edilecektir. A1’ in sadece ikinci teknik faulünün cezası uygulanacak olup diskalifiye için ek bir ceza verilmeyecektir. Sayı görevlisi A1'e 2 teknik faul verildiğinde diskalifiye edilmesi gerektiğini hemen bir hakeme bildirmelidir.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-19\nAçıklama: Bir oyuncu kişisel, teknik ya da sportmenlik dışı olarak beşinci faulünü aldığında oyun dışı kalmış bir oyuncu olur. Beşinci faulünden sonra kendisine verilecek diğer teknik fauller o oyuncunun başantrenörüne yazılacak ve ‘B1 ’ olarak kaydedilecektir. Oyun dışı kalmış oyuncu diskalifiye edilmiş bir oyuncu değildir ve takım sıra bölgesinde kalabilir.\nÖrnek 36-20: Birinci çeyrek sırasında B1’e (a) Bir teknik faul. (b) Sportmenlik dışı faul verilir. Dördüncü ç...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki durumda da B1 diskalifiye edilmeyecektir. Beşinci faulüyle B1 oyun dışı kalmış oyuncu olmuştur. B1’e verilecek diğer teknik fauller başantrenörüne yazılacak ve ‘B1 ’ olarak kaydedilecektir. Herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun A takımı tarafından B1’e çalınan son teknik faulün olduğu en yakın yerden topun oyuna sokulmasıyla devam edecektir.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-19\nAçıklama: Bir oyuncu kişisel, teknik ya da sportmenlik dışı olarak beşinci faulünü aldığında oyun dışı kalmış bir oyuncu olur. Beşinci faulünden sonra kendisine verilecek diğer teknik fauller o oyuncunun başantrenörüne yazılacak ve ‘B1 ’ olarak kaydedilecektir. Oyun dışı kalmış oyuncu diskalifiye edilmiş bir oyuncu değildir ve takım sıra bölgesinde kalabilir.\nÖrnek 36-21: B1 dripling yapan A1’e faul yapar. Bu B1’in beşinci ve B takımın o çeyrekteki ikinci takım faulü...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B1 diskalifiye edilmiştir ve soyunma odasına gidecek ya da eğer isterse salonu terk edecektir. B1’ e verilen diskalifiye edici faul maç kağıdında beşinci faulünden sonraki boşluğa ‘D’ olarak yazılacak ve başantrenörüne de ‘B2’ olarak kaydedilecektir. Herhangi bir A takımı oyuncusu kimse dizilmeden 2 serbest atış kullanacaktır. Oyun A takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-19\nAçıklama: Bir oyuncu kişisel, teknik ya da sportmenlik dışı olarak beşinci faulünü aldığında oyun dışı kalmış bir oyuncu olur. Beşinci faulünden sonra kendisine verilecek diğer teknik fauller o oyuncunun başantrenörüne yazılacak ve ‘B1 ’ olarak kaydedilecektir. Oyun dışı kalmış oyuncu diskalifiye edilmiş bir oyuncu değildir ve takım sıra bölgesinde kalabilir.\nÖrnek 36-22: B1 dripling yapan A1’e faul yapar. Bu, B1’in beşinci ve B takımın o çeyrekteki beşinci takım fau...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B1 diskalifiye edilmiştir ve soyunma odasına gidecek ya da eğer isterse salonu terk edecektir. B1’ e verilen diskalifiye edici faul maç kağıdında beşinci faulünden sonraki boşluğa ‘D’ olarak yazılacak ve başantrenörüne de ‘B2’ olarak kaydedilecektir. A1 kimse dizilmeden 2 serbest atış kullanacaktır. Daha sonra herhangi bir A takımı oyuncusu kimse dizilmeden 2 serbest atış kullanacaktır. Oyun A takımının ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-23\nAçıklama: Bir oyuncuya 1 teknik faul ve 1 sportmenlik dışı faul verildiğinde diskalifiye edilecektir.\nÖrnek 36-24: A1’e birinci devre sırasında oyunu geciktirdiği için bir teknik faul verilir. İkinci devre A1’e, B1’e yaptığı temasın gerekli kriterleri karşılaması sebebiyle bir sportmenlik dışı faul çalınır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bir oyuncuya 1 teknik faul ve 1 sportmenlik dışı faul verildiğinde sayı hakeminin bir hakemi derhal bilgilendirmesi gerektiğinden bu durumda A1 otomatik olarak diskalifiye edilecektir. A1’in sadece sportmenlik dışı faulünün cezası uygulanacak diskalifiye için ek bir ceza verilmeyecektir. B1 kimse dizilmeden 2 serbest atış kullanacaktır. Oyun B takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-23\nAçıklama: Bir oyuncuya 1 teknik faul ve 1 sportmenlik dışı faul verildiğinde diskalifiye edilecektir.\nÖrnek 36-25: A1’e birinci devre sırasında hızlı geçiş hücumundaki takımının ilerleyişini durdurmak için yaptığı gereksiz bir temas nedeniyle bir sportmenlik dışı faul verilir. İkinci devre topun uzağındaki bir bölgede faul yapılmış aldatması yaptığı için A1’e bir teknik faul çalındığından A2, kendi geri sahasında dripling yapmaktadır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Bir oyuncuya 1 teknik faul ve 1 sportmenlik dışı faul verildiğinde sayı hakeminin bir hakemi derhal bilgilendirmesi gerektiğinden bu durumda A1 otomatik olarak diskalifiye edilecektir. A1’in sadece teknik faulünün cezası uygulanacak diskalifiye için ek bir ceza verilmeyecektir. Herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun A takımı tarafından teknik faul çalındığında topun olduğu en yakın yerden top oyuna sokmasıyla devam edecektir. A takımının şut saatinde kalan süresi kadar zamanı olacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-26\nAçıklama: Bir oyuncu-başantrenörüne aşağıdaki faullerin verilmesi durumunda otomatik olarak diskalifiye edilecektir. • Oyuncu olarak 2 teknik faul. • Oyuncu olarak 2 sportmenlik dışı faul. • Oyuncu olarak 1 sportmenlik dışı faul ve 1 teknik faul. • Başantrenör olarak ‘C1’ kaydedilen 1 teknik faul ve oyuncu olarak 1 sportmenlik dışı ya da teknik faul • Başantrenör olarak ‘B1’ ya da ‘B2’ kaydedilen 1 teknik faul, başantrenör olarak ‘C1’ kaydedilen bir teknik faul ve oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyuncu-başantrenörü A1, otomatik olarak diskalifiye edilecektir. Sadece kendi ikinci teknik faulünün cezası uygulanacak olup diskalifiye için ek ceza bir verilmeyecektir. Sayı görevlisi, bir oyuncu- başantrenörü olan A1’e, bir oyuncu olarak 1 teknik faul ve ardından bir başantrenör olarak 1 kişisel teknik faul verildiğinde, otomatik olarak diskalifiye edilmesi gerektiğini hemen bir hakeme bildirmelidir. Herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun A takımı tarafından, A1’e teknik faul çalındığında topun olduğu en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde, kalan süresi kadar zamanı olacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-26\nAçıklama: Bir oyuncu-başantrenörüne aşağıdaki faullerin verilmesi durumunda otomatik olarak diskalifiye edilecektir. • Oyuncu olarak 2 teknik faul. • Oyuncu olarak 2 sportmenlik dışı faul. • Oyuncu olarak 1 sportmenlik dışı faul ve 1 teknik faul. • Başantrenör olarak ‘C1’ kaydedilen 1 teknik faul ve oyuncu olarak 1 sportmenlik dışı ya da teknik faul • Başantrenör olarak ‘B1’ ya da ‘B2’ kaydedilen 1 teknik faul, başantrenör olarak ‘C1’ kaydedilen bir teknik faul ve oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyuncu-başantrenör A1 otomatik olarak diskalifiye edilecektir. Sadece kendi ikinci teknik faulünün cezası uygulanacak olup (yedek oyuncu A6’nın teknik faulü) diskalifiye için ek bir ceza verilmeyecektir. Sayı görevlisi, bir oyuncu-başantrenör olan A1’e bir oyuncu olarak 1 sportmenlik dışı faul ve bir başantrenör olarak takım sırası görevlisinden dolayı 2 teknik faul verildiğinde otomatik olarak diskalifiye edilmesi gerektiğini hemen bir hakeme bildirmelidir. Herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun A takımı tarafından A6’ya teknik faul çalındığında topun olduğu en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde kalan süresi kadar zamanı olacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-26\nAçıklama: Bir oyuncu-başantrenörüne aşağıdaki faullerin verilmesi durumunda otomatik olarak diskalifiye edilecektir. • Oyuncu olarak 2 teknik faul. • Oyuncu olarak 2 sportmenlik dışı faul. • Oyuncu olarak 1 sportmenlik dışı faul ve 1 teknik faul. • Başantrenör olarak ‘C1’ kaydedilen 1 teknik faul ve oyuncu olarak 1 sportmenlik dışı ya da teknik faul • Başantrenör olarak ‘B1’ ya da ‘B2’ kaydedilen 1 teknik faul, başantrenör olarak ‘C1’ kaydedilen bir teknik faul ve oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyuncu-başantrenörü A1 otomatik olarak diskalifiye edilecektir. Sadece kendi sportmenlik dışı faulünün cezası uygulanacak olup diskalifiye için ek bir ceza verilmeyecektir. Sayı görevlisi, bir oyuncu- başantrenörü olan A1’e, bir başantrenör olarak 1 kişisel teknik faul ve bir oyuncu olarak 1 sportmenlik dışı faul verildiğinde otomatik olarak diskalifiye edilmesi gerektiğini hemen bir hakeme bildirmelidir. B1 kimse dizilmeden 2 serbest atış kullanacaktır. Oyun B takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-26\nAçıklama: Bir oyuncu-başantrenörüne aşağıdaki faullerin verilmesi durumunda otomatik olarak diskalifiye edilecektir. • Oyuncu olarak 2 teknik faul. • Oyuncu olarak 2 sportmenlik dışı faul. • Oyuncu olarak 1 sportmenlik dışı faul ve 1 teknik faul. • Başantrenör olarak ‘C1’ kaydedilen 1 teknik faul ve oyuncu olarak 1 sportmenlik dışı ya da teknik faul • Başantrenör olarak ‘B1’ ya da ‘B2’ kaydedilen 1 teknik faul, başantrenör olarak ‘C1’ kaydedilen bir teknik faul ve oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Takım sıra bölgesinde oturmasına izin verilen diğer kişilerin sportmenlik dışı davranışları sonucunda verilen bir teknik faul, maç kağıdına birinci yardımcı antrenöre yazılmış olsa bile oyuncu- başantrenörüne işlenir.',
                'choices': [
                    ('İzin verilir', True),
                    ('izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-26\nAçıklama: Bir oyuncu-başantrenörüne aşağıdaki faullerin verilmesi durumunda otomatik olarak diskalifiye edilecektir. • Oyuncu olarak 2 teknik faul. • Oyuncu olarak 2 sportmenlik dışı faul. • Oyuncu olarak 1 sportmenlik dışı faul ve 1 teknik faul. • Başantrenör olarak ‘C1’ kaydedilen 1 teknik faul ve oyuncu olarak 1 sportmenlik dışı ya da teknik faul • Başantrenör olarak ‘B1’ ya da ‘B2’ kaydedilen 1 teknik faul, başantrenör olarak ‘C1’ kaydedilen bir teknik faul ve oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Maç kağıdına birinci yardımcı antrenör yazılmış olsa bile teknik fauller aşağıdaki gibi işlenir. (a) Oyuncu olarak A6’ya, (b) Oyuncu olarak A1’e, (c) Oyuncu-başantrenör olarak A1’e',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-26\nAçıklama: Bir oyuncu-başantrenörüne aşağıdaki faullerin verilmesi durumunda otomatik olarak diskalifiye edilecektir. • Oyuncu olarak 2 teknik faul. • Oyuncu olarak 2 sportmenlik dışı faul. • Oyuncu olarak 1 sportmenlik dışı faul ve 1 teknik faul. • Başantrenör olarak ‘C1’ kaydedilen 1 teknik faul ve oyuncu olarak 1 sportmenlik dışı ya da teknik faul • Başantrenör olarak ‘B1’ ya da ‘B2’ kaydedilen 1 teknik faul, başantrenör olarak ‘C1’ kaydedilen bir teknik faul ve oy...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyuncu-başantrenörü A1, oyuncu olarak 5 faul yapmadığı ve başantrenör olarak diskalifiye edilmediği sürece oyuncu olarak devam edebilir. Oyuncu-başantrenörü A1, oyuncu olarak 5 faul aldıktan sonra başantrenör olarak devam edebilir.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-33\nAçıklama: Dördüncü çeyrekte ve her uzatmada oyun saati 2:00 dakika ya da daha az gösterirken ve hakemin topu, oyuna sokacak olan oyuncunun kullanımına vermesi gerektiği durumlarda topu oyuna sokacak olan oyuncuyu savunun bir oyuncunun olduğu durumlarda aşağıdaki prosedür uygulanacaktır: • Hakemler, topu oyuna sokacak oyuncuya topu vermeden önce bir uyarı olarak “kural dışı sınır çizgisi geçişi” işaretini göstereceklerdir. • Eğer savunma oyuncusu topun oyuna sokulması...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Hakem topu A1’e vermeden önce B1’e uyarı işareti gösterdiğinden topun oyuna sokulmasına müdahalesi nedeniyle B1’e bir teknik faul verilecektir. Herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun A takımı tarafından B1’e teknik faul çalındığında topun olduğu en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde, (a) 14 saniyesi, eğer şut saati 13 saniye veya daha az gösteriyorsa, şut saati 14 saniye veya daha fazla süre gösteriyorsa kalan süre kadar zamanı olacaktır. (b) 24 saniyesi olacaktır.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-35\nAçıklama: İlk 3 çeyrek içerisinde ve oyun saati dördüncü çeyrek ile her uzatmada 2:00 dakikadan daha fazla süre gösterdiğinde topun oyuna sokulması durumu oluşabilir. Eğer savunma oyuncusu topun oyuna sokulmasına engellemek için vücudunun herhangi bir bölümünü sınır çizgisi üzerinden hareket ettirirse aşağıdaki prosedür uygulanacaktır. • Hakem oyunu derhal durduracak ve savunma oyuncusuna ile o takımın başantrenörüne sözlü uyarıda bulunacaktır. Bu uyarı oyunun geri k...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "(a) B takımı oyuncusu oyunda ilk kez topun oyuna sokulmasına müdahale ederse, hakemler oyunu derhal durduracak ve B1'e ve B takımı başantrenörüne sözlü uyarıda bulunacaktır. (b) Hakem oyunda herhangi bir B takımı oyuncusunu topun oyuna sokulmasına müdahale ettiği için sözlü olarak uyarmışsa, B1'e teknik faul verilecektir. Herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun, A takımı tarafından dip çizginin gerisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 24 saniyesi olacaktır.",
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-37\nAçıklama: Bir teknik faul çalındığında, serbest atış cezası kimse dizilmeden hemen yönetilecektir. Serbest atıştan sonra oyun, teknik faul çalındığında topun olduğu en yakın yerden devam edecektir.\nÖrnek 36-38: B1’e bir teknik faul verildiğinde A1, şut saatinde 21 saniyeyle kendi geri sahasında dripling yapmaktadır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun A takımı tarafından, teknik faul çalındığında topun olduğu en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının yeni bir 8 saniye sayımı için süresi ve şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-37\nAçıklama: Bir teknik faul çalındığında, serbest atış cezası kimse dizilmeden hemen yönetilecektir. Serbest atıştan sonra oyun, teknik faul çalındığında topun olduğu en yakın yerden devam edecektir.\nÖrnek 36-39: A2’ye bir teknik faul verildiğinde A1, şut saatinde 21 saniyeyle kendi geri sahasında dripling yapmaktadır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun A takımı tarafından, teknik faul çalındığında topun olduğu en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının topu ön sahaya götürmesi için 5 saniyesi olacaktır. A takımının şut saatinde 21 saniyesi olacaktır.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-37\nAçıklama: Bir teknik faul çalındığında, serbest atış cezası kimse dizilmeden hemen yönetilecektir. Serbest atıştan sonra oyun, teknik faul çalındığında topun olduğu en yakın yerden devam edecektir.\nÖrnek 36-40: B1, A1’e 2 sayılık atış girişimi sırasında faul yapar. Top sepetten içeri girmez. (a) A1’in ilk serbest atışından önce A2’ye bir teknik faul verilir. (b) A1’in ilk serbest atışından sonra A2’ye bir teknik faul verilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Herhangi bir B takımı oyuncusu ya da yedek oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Daha sonra A1, 2 serbest atış kullanacaktır. (b) Herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kulanacaktır. Daha sonra A1 ikinci serbest atışını kullanacaktır.',
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-37\nAçıklama: Bir teknik faul çalındığında, serbest atış cezası kimse dizilmeden hemen yönetilecektir. Serbest atıştan sonra oyun, teknik faul çalındığında topun olduğu en yakın yerden devam edecektir.\nÖrnek 36-41: Bir mola sırasında A2’e bir teknik faul verilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Mola tamamlanacaktır. Mola sonrasında, herhangi bir B takımı oyuncusu ya da yedek oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun, moladan önce oyunun durdurulduğu en yakın yerden devam edecektir.',
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-37\nAçıklama: Bir teknik faul çalındığında, serbest atış cezası kimse dizilmeden hemen yönetilecektir. Serbest atıştan sonra oyun, teknik faul çalındığında topun olduğu en yakın yerden devam edecektir.\nÖrnek 36-42: A1 ‘in sahadan sayı amacıyla attığı şut havadayken bir teknik faul çalınır: (a) B1’e veya B takımı doktoruna. (b) A2’ye veya A takımı doktoruna.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Serbest atışın: (a) Herhangi bir A takımı oyuncusu 1 serbest atış kullanacaktır, (b) Herhangi bir A takımı oyuncusu 1 serbest atış kullanacaktır, Eğer A1’in şutunda top sepete girerse sayı geçerli sayılacaktır. Oyun, B takımı tarafından dip çizginin gerisindeki herhangi bir yerden topu oyuna sokmasıyla devam edecektir. A1’in şutunda top sepete girmezse oyun pozisyon sırasına göre, teknik faulün meydana geldiği en yakın yerden topun oyuna sokulmasıyla devam edecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 36 Teknik faul | 36-37\nAçıklama: Bir teknik faul çalındığında, serbest atış cezası kimse dizilmeden hemen yönetilecektir. Serbest atıştan sonra oyun, teknik faul çalındığında topun olduğu en yakın yerden devam edecektir.\nÖrnek 36-43: A1 ‘in sahadan sayı amacıyla attığı şut havadayken bir teknik faul çalınır: (a) B takım doktoruna (b) A takım doktoruna\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Serbest atışın: (a) B takımı doktorunun teknik faulünden dolayı herhangi bir A oyuncusu tarafından, (b) A takımı doktorunun teknik faulünden dolayı herhangi bir B oyuncusu tarafından kullanılmasından sonra: A1’in şutunda top sepete girerse geçerli sayı sayılacaktır. Oyun, B takımı tarafından dip çizginin gerisindeki herhangi bir yerden topu oyuna sokmasıyla devam edecektir. A1’in şutunda top sepete girmezse oyun pozisyon sırasına göre, teknik faulün meydana geldiği en yakın yerden topun oyuna sokulmasıyla devam edecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 37 Sportmenlik dışı faul | 37-1\nAçıklama: Rakibin sepetine doğru ilerleyen bir hücum oyuncuyla birlikte top ve sepet arasında başka bir savunma oyuncu bulunmuyorsa, ilerleyişini sürdüren bu oyuncuya bir rakip oyuncunun arkadan veya yandan yaptığı kural dışı temas, sadece hücum oyuncusu atış haline başlayana kadar sportmenlik dışı olarak değerlendirilebilir. Ancak, kurallara uygun olarak, doğrudan topla oynamaya yönelik olmayan ya da herhangi bir aşırı, sert temas oyunun herhangi bir anında...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Bu, B1'in sportmenlik dışı faulüdür.",
                'choices': [
                    ("Bu, B1'in sportmenlik dışı faulüdür.", True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 37 Sportmenlik dışı faul | 37-1\nAçıklama: Rakibin sepetine doğru ilerleyen bir hücum oyuncuyla birlikte top ve sepet arasında başka bir savunma oyuncu bulunmuyorsa, ilerleyişini sürdüren bu oyuncuya bir rakip oyuncunun arkadan veya yandan yaptığı kural dışı temas, sadece hücum oyuncusu atış haline başlayana kadar sportmenlik dışı olarak değerlendirilebilir. Ancak, kurallara uygun olarak, doğrudan topla oynamaya yönelik olmayan ya da herhangi bir aşırı, sert temas oyunun herhangi bir anında...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Her iki durumda da bu, B1'in sportmenlik dışı faulüdür.",
                'choices': [
                    ("Her iki durumda da bu, B1'in sportmenlik dışı faulüdür.", True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 37 Sportmenlik dışı faul | 37-1\nAçıklama: Rakibin sepetine doğru ilerleyen bir hücum oyuncuyla birlikte top ve sepet arasında başka bir savunma oyuncu bulunmuyorsa, ilerleyişini sürdüren bu oyuncuya bir rakip oyuncunun arkadan veya yandan yaptığı kural dışı temas, sadece hücum oyuncusu atış haline başlayana kadar sportmenlik dışı olarak değerlendirilebilir. Ancak, kurallara uygun olarak, doğrudan topla oynamaya yönelik olmayan ya da herhangi bir aşırı, sert temas oyunun herhangi bir anında...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "(a) Bu, B1'in kişisel faulüdür. (b) Bu, B1'in sportmenlik dışı faulüdür.",
                'choices': [
                    ('Kişisel faul', True),
                    ('Faul yok / oyun devam', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 37 Sportmenlik dışı faul | 37-1\nAçıklama: Rakibin sepetine doğru ilerleyen bir hücum oyuncuyla birlikte top ve sepet arasında başka bir savunma oyuncu bulunmuyorsa, ilerleyişini sürdüren bu oyuncuya bir rakip oyuncunun arkadan veya yandan yaptığı kural dışı temas, sadece hücum oyuncusu atış haline başlayana kadar sportmenlik dışı olarak değerlendirilebilir. Ancak, kurallara uygun olarak, doğrudan topla oynamaya yönelik olmayan ya da herhangi bir aşırı, sert temas oyunun herhangi bir anında...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Bu, A2'ye pas olarak top elden çıktıktan sonra A2 ile sepet arasında herhangi bir B takımı oyuncusu yokken ilerleyen bir oyuncuya arkadan veya yandan yapılan kural dışı temastan dolayı B1 tarafından yapılan sportmenlik dışı bir faulüdür.",
                'choices': [
                    ("Bu, A2'ye pas olarak top elden çıktıktan sonra A2 ile sepet arasında herhangi bir B takımı oyuncusu yokken ilerleyen bir oyuncuya arkadan veya yandan yapılan k…", True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 37 Sportmenlik dışı faul | 37-1\nAçıklama: Rakibin sepetine doğru ilerleyen bir hücum oyuncuyla birlikte top ve sepet arasında başka bir savunma oyuncu bulunmuyorsa, ilerleyişini sürdüren bu oyuncuya bir rakip oyuncunun arkadan veya yandan yaptığı kural dışı temas, sadece hücum oyuncusu atış haline başlayana kadar sportmenlik dışı olarak değerlendirilebilir. Ancak, kurallara uygun olarak, doğrudan topla oynamaya yönelik olmayan ya da herhangi bir aşırı, sert temas oyunun herhangi bir anında...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Bu, A2'ye topu pas olarak vermek için A1 topu elinden çıkarmadığından dolayı A2 ile sepet arasında B takımı oyuncusu yokken ilerleyen bir oyuncuya arkadan veya yandan kural dışı temas için B1 tarafından yapılan bir sportmenlik dışı faul değildir.",
                'choices': [
                    ("Bu, A2'ye topu pas olarak vermek için A1 topu elinden çıkarmadığından dolayı A2 ile sepet arasında B takımı oyuncusu yokken ilerleyen bir oyuncuya arkadan veya…", True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 37 Sportmenlik dışı faul | 37-1\nAçıklama: Rakibin sepetine doğru ilerleyen bir hücum oyuncuyla birlikte top ve sepet arasında başka bir savunma oyuncu bulunmuyorsa, ilerleyişini sürdüren bu oyuncuya bir rakip oyuncunun arkadan veya yandan yaptığı kural dışı temas, sadece hücum oyuncusu atış haline başlayana kadar sportmenlik dışı olarak değerlendirilebilir. Ancak, kurallara uygun olarak, doğrudan topla oynamaya yönelik olmayan ya da herhangi bir aşırı, sert temas oyunun herhangi bir anında...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Bu, B1 ile sepet arasında başka hiçbir A takımı oyuncusu yokken, B1 topun kontrolünü ele geçirmeye çalışırken A2'nin B1'e arkadan veya yandan kural dışı teması nedeniyle yaptığı sportmenlik dışı fauldür.",
                'choices': [
                    ("Bu, B1 ile sepet arasında başka hiçbir A takımı oyuncusu yokken, B1 topun kontrolünü ele geçirmeye çalışırken A2'nin B1'e arkadan veya yandan kural dışı teması…", True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': "Madde 37 Sportmenlik dışı faul | 37-8\nAçıklama: Bir oyuncu, beşinci kişisel faulünü yaptıktan sonra oyun dışı oyuncu olur. Bu oyuncuya verilecek başka herhangi bir teknik ya da diskalifiye edici faul veya sportmenlik dışı davranış faulü, başantrenöre 'B' olarak kaydedilecek ve buna göre cezalandırılacaktır.\nÖrnek 37-9: B1, dripling yapan A1'e faul yapar. Bu, B1’in beşinci kişisel faulü ve B takımının o çeyrekteki ikinci takım faulüdür. Takım sırasına giderken B1, A2'yi iter.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Beşinci faulü ile B1, oyun dışı oyuncu olmuştur. B1'in sportmenlik dışı davranışı, B takımı başantrenörüne bir teknik faul olarak verilecek ve 'B1' olarak kaydedilecektir. Herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun A takımı tarafından, B1'in sportmenlik dışı davranışı gerçekleştiğinde topun bulunduğu en yakın yerden topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': "Madde 37 Sportmenlik dışı faul | 37-8\nAçıklama: Bir oyuncu, beşinci kişisel faulünü yaptıktan sonra oyun dışı oyuncu olur. Bu oyuncuya verilecek başka herhangi bir teknik ya da diskalifiye edici faul veya sportmenlik dışı davranış faulü, başantrenöre 'B' olarak kaydedilecek ve buna göre cezalandırılacaktır.\nÖrnek 37-10: Dripling yapan A1, B1'e faul yapar. Takım sıra bölgesine giderken A1'e, bir hakeme sözlü hakaret ettiği için teknik faul verilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Beşinci faulü ile A1, oyun dışı oyuncu olmuştur. A1'in teknik faulü, A takımı başantrenörüne verilecek ve 'B1' olarak kaydedilecektir. Herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun B takımı tarafından A1'in takım faulünün olduğu en yakın yerden topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': "Madde 37 Sportmenlik dışı faul | 37-8\nAçıklama: Bir oyuncu, beşinci kişisel faulünü yaptıktan sonra oyun dışı oyuncu olur. Bu oyuncuya verilecek başka herhangi bir teknik ya da diskalifiye edici faul veya sportmenlik dışı davranış faulü, başantrenöre 'B' olarak kaydedilecek ve buna göre cezalandırılacaktır.\nÖrnek 37-11: A1, B1'e faul yapar. Bu, A1'in beşinci faulü ve A takımının o çeyrekteki ikinci takım faulüdür. Takım sırasına giderken A1, B1'i iter. Sonra B1, A1'i iter. B1, bir sportmenlik dı...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Beşinci faulü ile A1, oyun dışı oyuncu olmuştur. A1\'in sportmenlik dışı davranışı, A takımı başantrenörüne bir teknik faul olarak verilecek ve \'B1\' olarak kaydedilecektir. B1’in sportmenlik dışı faulü kendisine verilecek ve "U2" olarak kaydedilecektir. Herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. A1\'in yerine giren yedek oyuncu, kimse dizilmeden 2 serbest atış kullanacaktır. Oyun A takımı tarafından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 38 Diskalifiye edici faul | 38-1\nAçıklama: Diskalifiye edilen herhangi bir kişinin, artık takım sırasına oturmasına izin verilmez. Bu nedenle, herhangi bir sportmenlik dışı davranış nedeniyle artık cezalandırılamaz.\nÖrnek 38-2: A1, bariz bir sportmenlik dışı davranışından dolayı diskalifiye edilir. Oyun sahasını terk eder ve bir hakeme sözlü hakaret eder.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1 zaten diskalifiye edilmiştir ve sözlü hakaretlerinden dolayı artık cezalandırılamaz. Hakem ya da varsa komiser olayı anlatan bir raporu yarışmanın organizasyon birimine gönderecektir.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 38 Diskalifiye edici faul | 38-3\nAçıklama: Bir oyuncu bariz bir sportmenlik dışı davranışından dolayı diskalifiye edildiğinde cezası, diğer herhangi bir diskalifiye edici faulle aynıdır.\nÖrnek 38-4: A1, bir yürüme ihlali yapar. Moral bozukluğuyla sinirlenerek bir hakeme sözlü hakaret eder. A1’e diskalifiye edici faul verilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1, diskalifiye olmuş oyuncu olur. Diskalifiye edici faul A1’in kendisine verilir ve ‘D2’ olarak kaydedilir. Herhangi bir B takımı oyuncusu kimse dizilmeden 2 serbest atış kullanacaktır. Oyun, B takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 38 Diskalifiye edici faul | 38-5\nAçıklama: Başantrenör bir diskalifiye edici faulle cezalandırıldığında, "D2" olarak kaydedilecektir. Takım sırasına oturmasına izin verilen herhangi bir kişi diskalifiye edildiğinde başantrenöre, ‘B2’ kaydedilen bir teknik faul verilecektir. Cezası, diğer herhangi bir diskalifiye edici faulle aynı olacaktır.\nÖrnek 38-6: A1’e beşinci kişisel faulü verilir. Bu A takımının o çeyrekteki ikinci takım faulüdür. Takım sıra bölgesine giderken (a) A1, bir hakeme söz...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A1, beşinci kişisel faulü ile oyun dışı oyuncu olmuştur. A1, bir hakeme sözlü tacizde bulunduğu ya da B2’ye yumruk attığı için diskalifiye edilmiş bir oyun dışı oyuncu olmuştur. A1'in diskalifiye edici faulü maç kağıdına, A1'e 'D' olarak ve A takımının başantrenörüne de 'B2' olarak kaydedilecektir. (a) Herhangi bir B takımı oyuncusu kimse dizilmeden 2 serbest atış kullanacaktır. (b) B2 kimse dizilmeden 2 serbest atış kullanacaktır. Her iki durumda da oyun B takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 38 Diskalifiye edici faul | 38-7\nAçıklama: Bir oyuncunun veya takım sırasında oturmasına izin verilen bir kişinin sportmenliğe aykırı herhangi bir hareketi diskalifiye edici fauldür. Diskalifiye edici faul şu davranışlarının bir sonucu olabilir: • Rakip takımdan bir kişiye, hakemlere, masa görevlilerine ve komisere ya da seyirciye yönelik yapılan. • Kendi takımının herhangi bir üyesine yönelik yapılan. • Oyun donanımına kasıtlı olarak zarar vermek için yapılan.\nÖrnek 38-8: Aşağıdaki bariz ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "(a) ve (b) A1, diskalifiye edilecektir. Diskalifiye edici faul A1’in kendisine verilir ve ‘D2’ olarak kaydedilir. (c) ve (d) A6, diskalifiye edilecektir. A6'nın diskalifiye edici faulü kendisine 'D' olarak ve A takımının başantrenörüne de 'B2' olarak kaydedilecektir. Herhangi bir B takımı oyuncusu kimse dizilmeden 2 serbest atış kullanacaktır. Oyun B takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': "Madde 38 Diskalifiye edici faul | 38-9\nAçıklama: Bir oyuncu diskalifiye edilirse ve soyunma odasına giderken sportmenlik dışı veya diskalifiye edici faulü hak edici bir şekilde hareket ederse, bu ek davranışları cezalandırılmayacak ve sadece müsabakanın organizasyon birimine rapor edilecektir.\nÖrnek 38-10: A1, bir hakeme sözlü hakarette bulunduğu için diskalifiye edici faulle cezalandırılır. Soyunma odasına doğru giderken: (a) A1, bir sportmenlik dışı faulü hak edecek şekilde B1'i iter. (b) A1, ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "A1, diskalifiye edildikten sonra ilave faul verilemez ve cezalandırılamaz. A1’in davranışı, başhakem veya varsa komiser tarafından müsabakanın organizasyon birimine rapor edilecektir. Her iki durumda da B takımına, A1'in diskalifiye edici faulünden dolayı kimse dizilmeden 2 serbest atış hakkı verilecektir. Oyun B takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 39 Kavga | 39-1\nAçıklama: Kavgadan sonra tüm cezalar birbirini iptal ederse, kavga başladığında topu kontrol etmekte olan ya da topa sahip olma hakkı olan takıma, kavga başladığında topun olduğu en yakın yerden topu oyuna sokma hakkı verilecektir. Takımın şut saatinde, oyun durdurulduğunda kalan süresi kadar zamanı olacaktır.\nÖrnek 39-2: A takımı, oyun sahasında kavgaya yol açabilecek bir durum meydana geldiğinde, aşağıda belirtilen süre boyunca topu kontrol etmiştir: (a) 20 saniye, (b) 5 ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun, kavga başlamadan önce topu kontrol eden A takımı tarafından, kavga başladığında topun olduğu en yakın yerden topu oyuna sokmasıyla devam edecektir. Şut saatinde: (a) 4 saniyeyle, (b) 19 saniyeyle.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "Madde 39 Kavga | 39-3\nAçıklama: Kendisi, birinci yardımcı antrenör (eğer biri ya da her ikisi de düzeni sağlamak ve korumak için hakemlere yardım etmezlerse), yedek oyuncu, oyun dışı oyuncusu ya da delegasyon üyesi, bir kavga sırasında takım sıra bölgesini terk ettiği için diskalifiye edilirse, o takımının başantrenörüne tek bir teknik faul verilecektir. Teknik faul, başantrenörün diskalifiye edilmesini içeriyorsa, maç kağıdına 'D2' olarak kaydedilecektir. Teknik faul sadece takım sırasına oturm...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "A6’nın diskalifiyesi kendisine 'D' olarak ve kalan faul boşlukları ise 'F' olarak doldurularak kaydedilecektir. A takımı başantrenörüne 'B2' olarak kaydedilen bir teknik faul verilecektir. Herhangi bir B takımı oyuncusu kimse dizilmeden 2 serbest atış kullanacaktır. Oyun B takımı tafarından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': "Madde 39 Kavga | 39-3\nAçıklama: Kendisi, birinci yardımcı antrenör (eğer biri ya da her ikisi de düzeni sağlamak ve korumak için hakemlere yardım etmezlerse), yedek oyuncu, oyun dışı oyuncusu ya da delegasyon üyesi, bir kavga sırasında takım sıra bölgesini terk ettiği için diskalifiye edilirse, o takımının başantrenörüne tek bir teknik faul verilecektir. Teknik faul, başantrenörün diskalifiye edilmesini içeriyorsa, maç kağıdına 'D2' olarak kaydedilecektir. Teknik faul sadece takım sırasına oturm...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'A1 ve B1 diskalifiye edilecek ve \'DC’ olarak kaydedilecektir. A7 diskalifiye edilecek ve \'D2\' olarak kaydedilecektir. A7’nin maç kağıdında kalan faul alanları \'F\' olarak doldurulacaktır. A6 ve B6, bir kavga sırasında oyun sahasına girdikleri için diskalifiye edilecek ve \'D\' olarak kaydedilecektir. A6’nin ve B6’nın maç kağıdında kalan faul boşlukları \'F\' olarak doldurulacaktır. A takımı başantrenörü ve B takımı başantrenörü, \'BC\' olarak kaydedilen teknik faullerle cezalandırılacaktır. Diskalifiye edici faullerin (A1, B1) ve her iki teknik faulün (A6, B6) cezaları birbirini iptal edecektir. A7’nin kavgaya aktif olarak katılımından dolayı "D2 " olarak girilen diskalifiyenin cezası uygulanacaktır. B1\'in yerine giren yedek oyuncu, kimse dizilmeden 2 serbest atış kullanacaktır. Oyun B takımı tarafından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': "Madde 39 Kavga | 39-3\nAçıklama: Kendisi, birinci yardımcı antrenör (eğer biri ya da her ikisi de düzeni sağlamak ve korumak için hakemlere yardım etmezlerse), yedek oyuncu, oyun dışı oyuncusu ya da delegasyon üyesi, bir kavga sırasında takım sıra bölgesini terk ettiği için diskalifiye edilirse, o takımının başantrenörüne tek bir teknik faul verilecektir. Teknik faul, başantrenörün diskalifiye edilmesini içeriyorsa, maç kağıdına 'D2' olarak kaydedilecektir. Teknik faul sadece takım sırasına oturm...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "A1 ve B1 diskalifiye edilecek ve 'DC' ' olarak kaydedilecektir. Her iki diskalifiye edici faulün (A1, B1) cezaları birbirini iptal edecektir. A takımı başantrenörüne, takım sıra bölgesinden ayrılan A6 ve A takımı menajerinden dolayı 'B2' olarak kaydedilen bir teknik faul verilecektir. A6, kavgaya aktif olarak katılımından dolayı diskalifiye edilecek ve 'D2' olarak kaydedilecektir. A6’nın maç kağıdında kalan faul boşlukları 'F' olarak doldurulacaktır. Kavgaya aktif olarak katılımından dolayı A takımı menajerinin diskalifiye edici faulü başantrenörüne verilecek ve daire içine alınmış ‘B2' olarak kaydedilecek ve başantrenörün olası oyundan diskalifiye edilmesine sayılmayacaktır. Herhangi bir B takımı oyuncusu ya da oyuncuları 6 serbest atış kullanacaktır (A6 ve A takımı menajerinin takım sıra bölgesinden ayrılması sebebiyle başantrenöre verilen teknik faulden dolayı kimse dizilmeden 2 serbest atış, A6’nın kavgaya aktif olarak karışması sebebiyle kendisine verilen diskalifiyeden dolayı kimse dizilmeden 2 serbest atış, A takımı menajerinin kavgaya aktif olarak katılmasından dolayı başantrenöre verilen teknik faul sebebiyle kimse dizilmeden 2 serbest atış). Oyun B takımı tarafından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': "Madde 39 Kavga | 39-3\nAçıklama: Kendisi, birinci yardımcı antrenör (eğer biri ya da her ikisi de düzeni sağlamak ve korumak için hakemlere yardım etmezlerse), yedek oyuncu, oyun dışı oyuncusu ya da delegasyon üyesi, bir kavga sırasında takım sıra bölgesini terk ettiği için diskalifiye edilirse, o takımının başantrenörüne tek bir teknik faul verilecektir. Teknik faul, başantrenörün diskalifiye edilmesini içeriyorsa, maç kağıdına 'D2' olarak kaydedilecektir. Teknik faul sadece takım sırasına oturm...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "A takımı başantrenörüne, takım sırası bölgesini terk ettiği ve hakemlere düzeni tekrar sağlamak ve korumak için yardımcı olmadığından dolayı maç kağıdına ' D2' olarak kaydedilecek bir diskalifiye edici faul verilir. A takımı başantrenörüne, kavgaya aktif olarak katılımı nedeniyle başka bir diskalifiye edici faul verilmeyecektir. A takımı başantrenörünün kalan faul boşlukları 'F' olarak doldurulacaktır. Herhangi bir B takımı oyuncusu kimse dizilmeden 2 serbest atış kullanacaktır. Oyun B takımı tarafından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': "Madde 39 Kavga | 39-3\nAçıklama: Kendisi, birinci yardımcı antrenör (eğer biri ya da her ikisi de düzeni sağlamak ve korumak için hakemlere yardım etmezlerse), yedek oyuncu, oyun dışı oyuncusu ya da delegasyon üyesi, bir kavga sırasında takım sıra bölgesini terk ettiği için diskalifiye edilirse, o takımının başantrenörüne tek bir teknik faul verilecektir. Teknik faul, başantrenörün diskalifiye edilmesini içeriyorsa, maç kağıdına 'D2' olarak kaydedilecektir. Teknik faul sadece takım sırasına oturm...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': '(a) Mola nedeniyle hali hazırda sahada olan hiç kimse diskalifiye edilmeyecektir. (b) Mola nedeniyle sahada bulunan ve takım sıralarının yakınındaki yerlerini terk eden tüm kişiler ve kavgaya yol açabilecek duruma aktif olarak dahil olan tüm oyuncular diskalifiye edilecektir.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 42 Özel durumlar | 42-1\nAçıklama: Aynı duran saat periyodu sırasında yönetilecek birçok cezayı içeren özel durumlarda hakemler, hangi cezaların uygulanacağını ve hangi cezaların iptal edileceğini belirlerken, ihlal ve faullerin hangi sırayla gerçekleştiğine özellikle dikkat etmelidirler.\nÖrnek 42-2: B1, şut atan A1’e bir sportmenlik dışı faul yapar. Top havadayken şut saati sesli işaret verir. Sonrasında: (a) Top çembere temas etmez. (b) Top sadece çembere temas eder, ancak sepete girmez. ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Tüm durumlarda B1'in sportmenlik dışı faulü göz ardı edilemez. (a) A takımının şut saati ihlali, sportmenlik dışı faulden sonra olduğu için dikkate alınmayacaktır (top çembere temas etmese de). A1, kimse dizilmeden 2 ya da 3 serbest atış kullanacaktır. (b) Bu durum A takımının şut saati ihlali değildir. A1, kimse dizilmeden 2 ya da 3 serbest atış kullanacaktır. (c) A1’e 2 ya da 3 sayı ile birlikte kimse dizilmeden 1 ek serbest atış hakkı verilecektir. Tüm durumlarda oyun A takımı tarafından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.",
                'choices': [
                    ('Şut saati ihlali: Top A takımına verilir', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'Madde 42 Özel durumlar | 42-1\nAçıklama: Aynı duran saat periyodu sırasında yönetilecek birçok cezayı içeren özel durumlarda hakemler, hangi cezaların uygulanacağını ve hangi cezaların iptal edileceğini belirlerken, ihlal ve faullerin hangi sırayla gerçekleştiğine özellikle dikkat etmelidirler.\nÖrnek 42-3: B1, sahadan sayı amacıyla atış halinde olan A1’e bir faul yapar. Faulün ardından A1, hala atış halindeyken B2 tarafından faul yapılır.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B2’in faulü bir sportmenlik dışı ve diskalifiye edici faul olmadıkça dikkate alınmayacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 42 Özel durumlar | 42-1\nAçıklama: Aynı duran saat periyodu sırasında yönetilecek birçok cezayı içeren özel durumlarda hakemler, hangi cezaların uygulanacağını ve hangi cezaların iptal edileceğini belirlerken, ihlal ve faullerin hangi sırayla gerçekleştiğine özellikle dikkat etmelidirler.\nÖrnek 42-4: B1, dripling yapan A1’e bir sportmenlik dışı faul yapar. Faulün ardında, A ve B takımı başantrenörlerine teknik faul verilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '2 başantrenörün teknik faulleri için olan eşit cezalar iptal edilecektir. A1 kimse dizilmeden 2 serbest atış kullanacaktır. Oyun A takımı tarafından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 42 Özel durumlar | 42-1\nAçıklama: Aynı duran saat periyodu sırasında yönetilecek birçok cezayı içeren özel durumlarda hakemler, hangi cezaların uygulanacağını ve hangi cezaların iptal edileceğini belirlerken, ihlal ve faullerin hangi sırayla gerçekleştiğine özellikle dikkat etmelidirler.\nÖrnek 42-5: B1, başarılı şutunda A1’e faul yapar. Daha sonra A1’e bir teknik faul verilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in sayısı geçerli sayılacaktır. Her iki faulün cezaları eşittir ve birbirini iptal eder. Oyun, herhangi bir başarılı sayı sonrasında olduğu gibi devam edecektir.',
                'choices': [
                    ('A1’in sayısı geçerli sayılacaktır. Her iki faulün cezaları eşittir ve birbirini iptal eder. Oyun, herhangi bir başarılı sayı sonrasında olduğu gibi devam edece…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "Madde 42 Özel durumlar | 42-1\nAçıklama: Aynı duran saat periyodu sırasında yönetilecek birçok cezayı içeren özel durumlarda hakemler, hangi cezaların uygulanacağını ve hangi cezaların iptal edileceğini belirlerken, ihlal ve faullerin hangi sırayla gerçekleştiğine özellikle dikkat etmelidirler.\nÖrnek 42-6: B1, başarılı şutunda A1’e faul yapar. Daha sonra A1'e bir teknik faul verilir, ardından B takımı başantrenörüne teknik faul verilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "A1'in sayısı geçerli sayılacaktır. Tüm faullerin cezaları eşittir ve çalındıkları sırayla iptal edilecektir. B1'in kişisel faulü ve A1'in teknik faulünün cezaları birbirini iptal eder. B takımı başantrenörünün teknik faulünden dolayı, herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Oyun, herhangi bir başarılı sayı sonrasında olduğu gibi devam edecektir.",
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 42 Özel durumlar | 42-1\nAçıklama: Aynı duran saat periyodu sırasında yönetilecek birçok cezayı içeren özel durumlarda hakemler, hangi cezaların uygulanacağını ve hangi cezaların iptal edileceğini belirlerken, ihlal ve faullerin hangi sırayla gerçekleştiğine özellikle dikkat etmelidirler.\nÖrnek 42-7: B1, başarılı şutunda A1’e sportmenlik dışı faul yapar. Daha sonra A1’e bir teknik faul verilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1’in sayısı geçerli sayılacaktır. Her iki faulün cezaları eşit değildir ve birbirini iptal etmez. Herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. A1, kimse dizilmeden 1 serbest atış kullanacaktır. Oyun A takımı tarafından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 42 Özel durumlar | 42-1\nAçıklama: Aynı duran saat periyodu sırasında yönetilecek birçok cezayı içeren özel durumlarda hakemler, hangi cezaların uygulanacağını ve hangi cezaların iptal edileceğini belirlerken, ihlal ve faullerin hangi sırayla gerçekleştiğine özellikle dikkat etmelidirler.\nÖrnek 42-8: B1, A takımının ön sahasında dripling yapan A1’e faul yapar. (a) Bu, B takımının o çeyrekte üçüncü takım faulüdür. (b) Bu, B takımının o çeyrekte beşinci takım faulüdür. A1 daha sonra topu, B1’...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B 1’e bir kişisel faul verilir. A1’e bir teknik faul verilir. Herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. (a) Oyun A takımı tarafından, B1’in faulünün çalındığı en yakın yerden topu oyuna sokmasıyla devam edecektir. Şut saatinde 14 saniye veya daha fazla gösteriliyorsa, A takımının şut saatinde kalan süresi olacaktır. Şut saatinde 13 saniye veya daha az gösteriliyorsa, A takımının şut saatinde 14 saniyesi olacaktır. (b) A1, 2 serbest atış kullanacaktır. Oyun herhangi bir son serbest atıştan sonra olduğu gibi devam edecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 42 Özel durumlar | 42-1\nAçıklama: Aynı duran saat periyodu sırasında yönetilecek birçok cezayı içeren özel durumlarda hakemler, hangi cezaların uygulanacağını ve hangi cezaların iptal edileceğini belirlerken, ihlal ve faullerin hangi sırayla gerçekleştiğine özellikle dikkat etmelidirler.\nÖrnek 42-9: B1, dripling yapan A1’e faul yapar. (a) Bu, B takımının o çeyrekte üçüncü takım faulüdür. (b) Bu, B takımının o çeyrekte beşinci takım faulüdür. A1 daha sonra topu, yakın mesafeden doğrudan B1’...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B1’e bir kişisel faul verilir. A1’e temassız bir hareketinden dolayı diskalifiye edici faul verilir. (a) A takımının topa sahip olma hakkı, yönetilecek başka bir ceza olduğu için iptal edilir. (b) A1’in yerine giren yedek oyuncu kimse dizilmeden 2 serbest atış kullanacaktır. Her iki durumda da herhangi bir B takımı oyuncusu kimse dizilmeden 2 serbest atış kullanacaktır. Oyun B takımı tarafından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 42 Özel durumlar | 42-1\nAçıklama: Aynı duran saat periyodu sırasında yönetilecek birçok cezayı içeren özel durumlarda hakemler, hangi cezaların uygulanacağını ve hangi cezaların iptal edileceğini belirlerken, ihlal ve faullerin hangi sırayla gerçekleştiğine özellikle dikkat etmelidirler.\nÖrnek 42-10: Şut saatinde 8 saniye kala B1 kendi geri sahasında A1’e bir faul yapar. Ardından B2’ye bir teknik faul verilir. (a) B1’in faulü, B takımının o çeyrekteki dördüncü takım faulü ve B2’nin teknik ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Tüm durumlarda B2’nin teknik faulünden dolayı herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Serbest atıştan sonra, (a) Oyun A takımı tarafından, A1 için faul çalınan en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır. (b) A1, 2 serbest atış kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir. (c) A1, 2 ya da 3 serbest atış kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir. (d) A1’in sayısı geçerli sayılacaktır. A1, 1 serbest atış kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 42 Özel durumlar | 42-1\nAçıklama: Aynı duran saat periyodu sırasında yönetilecek birçok cezayı içeren özel durumlarda hakemler, hangi cezaların uygulanacağını ve hangi cezaların iptal edileceğini belirlerken, ihlal ve faullerin hangi sırayla gerçekleştiğine özellikle dikkat etmelidirler.\nÖrnek 42-11: B1, şut saatinde 8 saniye kala A1’e bir sportmenlik dışı faul yapar. Daha sonra; (a) A2’ye bir teknik faul verilir (b) B2’ye bir teknik faul verilir\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Herhangi bir B takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. (b) Herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Her iki durumda da teknik faul için olan serbest atıştan sonra A1, kimse dizilmeden 2 serbest atış kullanacaktır. Oyun A takımı tarafından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': "Madde 42 Özel durumlar | 42-12\nAçıklama: Serbest atış atıldığı sırada bir çift faul ya da cezaları eşit olan fauller olursa, fauller maç kağıdına kaydedilecek, ancak cezaları yönetilmeyecektir.\nÖrnek 42-13: A1’e 2 serbest atış hakkı verilir. (a) İlk serbest atıştan sonra, (b) Son başarılı serbest atıştan sonra top canlanmadan önce A2 ve B2'ye çift faul veya teknik faul verilir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "A2’nin ve B2'nin eşit faul cezaları iptal edilecektir. A1, ikinci serbest atışını kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir.",
                'choices': [
                    ("A2’nin ve B2'nin eşit faul cezaları iptal edilecektir. A1, ikinci serbest atışını kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi dev…", True),
                    ('1 serbest atış', False),
                    ('0 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 42 Özel durumlar | 42-14\nAçıklama: Bir teknik faul çalındığında, serbest atış cezası kimse dizilmeden hemen yönetilecektir. Bu, takım sırasına oturmasına izin verilen herhangi başka bir kişinin diskalifiye edilmesi nedeniyle başantrenöre verilen bir teknik faul için geçerli değildir. Bu tür bir teknik faulün cezası, iptal edilmediği sürece (2 serbest atış ve takımın ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokması), tüm fauller ve ihlaller meydana geldiği sıraya göre yönetile...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A6, bir kavga sırasında oyun sahasına girdiği için diskalifiye edilecektir. A takımı başantrenörüne 'B2' kaydedilen bir teknik faul verilecektir. A1, kimse dizilmeden 2 serbest atış kullanacaktır. Herhangi bir B takımı oyuncusu, A takımı başantrenörünün teknik faulünden dolayı kimse dizilmeden 2 serbest atış kullanacaktır. Oyun B takımı tarafından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'Madde 42 Özel durumlar | 42-16\nAçıklama: Bir çift faul ve her iki takımın eşit cezalarının iptal edilmesi durumundan sonra yönetilecek başka ceza kalmamışsa oyun, ilk ihlal olmadan önce topu kontrol eden ya da topu kontrol etme hakkı olan takım tarafından, topu oyuna sokmasıyla devam edecektir. İlk ihlalden önce hiçbir takımın topu kontrol etmediği veya hiçbir takımın topu kontrol etme hakkı olmaması durumunda bu, bir hava atışı durumudur. Oyun, pozisyon sırasına göre topun oyuna sokulmasıyla de...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Her iki takıma verilen eşit cezalar iptal edilecektir. Her iki durumda da oyun, bir sonraki topa sahip olma hakkına sahip takımın orta çizgi uzantısından topu oyuna sokmasıyla devam edecektir. Topa sahadaki bir oyuncuya temas ettiğinde veya kurala uygun olarak topa temas edildiğinde ok yönü rakip takım lehine değiştirilecektir.',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'Madde 42 Özel durumlar | 42-16\nAçıklama: Bir çift faul ve her iki takımın eşit cezalarının iptal edilmesi durumundan sonra yönetilecek başka ceza kalmamışsa oyun, ilk ihlal olmadan önce topu kontrol eden ya da topu kontrol etme hakkı olan takım tarafından, topu oyuna sokmasıyla devam edecektir. İlk ihlalden önce hiçbir takımın topu kontrol etmediği veya hiçbir takımın topu kontrol etme hakkı olmaması durumunda bu, bir hava atışı durumudur. Oyun, pozisyon sırasına göre topun oyuna sokulmasıyla de...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Her iki ihlal de aynı duran saat periyodunda meydana gelmiştir ve; (a) Top B takımı tarafından oyuna sokulması için canlanmadan önce. Bu nedenle eşit cezalar iptal edilecektir. A takımı ilk kural ihlalden önce topu kontrol ettiğinden dolayı oyun, A takımı tarafından A1'in faulünün veya ihlalinin olduğu en yakın yerden topun oyuna sokulması devam edecektir. A takımının şut saatinde kalan süresi kadar zamanı olacaktır. (b) Top B takımı tarafından oyuna sokulması için canlandıktan sonra. Bu andan itibaren ilk ihlalin cezası iptal için kullanılamaz. B2'nin faulünden dolayı topu oyuna sokma cezası, A1'in ihlali nedeniyle topa önceden sahip olma hakkını iptal eder. Oyun B2'nin faulünün meydana geldiği en yakın yerden A takımının topu oyuna sokmasıyla devam edecektir. Eğer kendi geri sahasındaysa A takımının şut saatinde 24 saniyesi olacaktır. Eğer kendi ön sahasındaysa A takımının şut saatinde 14 saniyesi olacaktır.",
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 43 Serbest atışlar | 43-1\nAçıklama: Serbest atış ribaund yerlerinde bulunan oyuncular, bu boşluklarda dönüşümlü olarak yer alma hakkına sahip olacaktır. Serbest atış ribaund yerlerinde olmayan oyuncular, serbest atış bitene kadar serbest atış çizgisi uzantısının ve 3 sayı çizgisinin gerisinde kalacaklardır.\nÖrnek 43-2: A1 son serbest atışını kullanır. B takımı oyuncularından hiçbiri, hakkı olan serbest atış ribaund yerlerine yerleşmezler.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Serbest atışlar sırasında oyuncular sadece hakları olan ribaund yerlerini kullanabilirler. Ribaund yerlerini kulanmayaya karar verirlerse, serbest atış bitene kadar serbest atış çizgisi uzantısının ve 3 sayı çizgisinin gerisinde kalacaklardır.',
                'choices': [
                    ('Serbest atışlar sırasında oyuncular sadece hakları olan ribaund yerlerini kullanabilirler. Ribaund yerlerini kulanmayaya karar verirlerse, serbest atış bitene …', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "Madde 43 Serbest atışlar | 43-3\nAçıklama: Son serbest atış sırasında her iki takımın oyuncuları da serbest atış ihlali yaparsa, bu bir hava atışı durumudur.\nÖrnek 43-4: B2, son serbest atışta top A1'in ellerinden çıkmadan önce kısıtlamalı alana girer. A1'in serbest atışı çembere değmez.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Bu, B2 ve A1'in serbest atış ihlalidir. Bir hava atışı durumu oluşur.",
                'choices': [
                    ("Bu, B2 ve A1'in serbest atış ihlalidir. Bir hava atışı durumu oluşur.", True),
                    ('1 serbest atış', False),
                    ('0 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-1\nAçıklama: Bir hatanın düzeltilebilmesi için hata, hakemler, masa görevlileri ya da varsa komiser tarafından, hatanın ardından oyun saati başladıktan sonraki ilk ölü topu takip eden topun canlanmasından önce fark edilmelidir. Hata, bir ölü top sırasında meydana gelir Hata düzeltilebilir Top canlanır Hata düzeltilebilir Oyun saati başlar ya da çalışmaya devam eder Hata düzeltilebilir Top ölür Hata düzeltilebilir Top canlanır Hata artık düzeltilemez Hatanın dü...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B2’nin sayısı geçerli sayılacaktır. (a) Hata hala düzeltilebilir. Serbest atışlar, atılıp atılmadığına bakılmaksızın iptal edilecektir. Oyun herhangi bir başarılı atıştan sonra olduğu gibi A takımının kendi dip çizgisinin gerisinden topu oyuna sokmasıyla devam edecektir. (b) Hata artık düzeltilemez. Oyun devam edecektir.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-1\nAçıklama: Bir hatanın düzeltilebilmesi için hata, hakemler, masa görevlileri ya da varsa komiser tarafından, hatanın ardından oyun saati başladıktan sonraki ilk ölü topu takip eden topun canlanmasından önce fark edilmelidir. Hata, bir ölü top sırasında meydana gelir Hata düzeltilebilir Top canlanır Hata düzeltilebilir Oyun saati başlar ya da çalışmaya devam eder Hata düzeltilebilir Top ölür Hata düzeltilebilir Top canlanır Hata artık düzeltilemez Hatanın dü...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Oyun hemen durdurulacaktır. A1, kimse dizilmeden ikinci serbest atışını kullanacaktır. (a) Oyun B takımı tarafından, oyunun durdurulduğu en yakın yerden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 18 saniyesi olacaktır. (b) B3'ün sayısı geçerli olacaktır. Oyun, herhangi bir başarılı atıştan sonra A takımı tarafından kendi dip çizgisinin gerisinden topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-4\nAçıklama: Hata, yanlış oyuncunun serbest atış ya da atışları atması halinde oluşursa, serbest atış ya da atışlar iptal edilecektir. Oyun henüz başlamamışsa, yönetilecek başka ihlal cezaları olmadıkça top, serbest atış çizgisi uzantısından oyuna sokması için rakiplere verilecektir. Eğer oyun devam etmişse, hatanın düzeltilmesi için oyun durdurulacaktır. Hatanın düzeltilmesinden sonra oyun, hatanın düzeltilmesi için oyunun durdurulduğu en yakın yerden devam e...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Hata hemen düzeltilecektir. A takımına herhangi bir yaptırım uygulanmadan A1, 2 serbest atış kullanacaktır. (b) ve (c) 2 serbest atış iptal edilecektir. Oyun B takımı tarafından, geri sahasındaki serbest atış çizgisi uzantısından topu oyuna sokmasıyla devam edecektir. B1’in faulü sportmenlik dışı olursa, cezanın bir parçası olan topa sahip olma hakkı da iptal edilecektir. Oyun B takımı tarafından, geri sahasındaki serbest atış çizgisi uzantısından topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-4\nAçıklama: Hata, yanlış oyuncunun serbest atış ya da atışları atması halinde oluşursa, serbest atış ya da atışlar iptal edilecektir. Oyun henüz başlamamışsa, yönetilecek başka ihlal cezaları olmadıkça top, serbest atış çizgisi uzantısından oyuna sokması için rakiplere verilecektir. Eğer oyun devam etmişse, hatanın düzeltilmesi için oyun durdurulacaktır. Hatanın düzeltilmesinden sonra oyun, hatanın düzeltilmesi için oyunun durdurulduğu en yakın yerden devam e...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Başarılı olup olmadığına bakılmaksızın 2 serbest atış iptal edilecektir. A3’ün sayısı geçerli sayılacaktır. Oyun B takımı tarafından, hatayı düzeltmek için oyunun durdurulduğu en yakın yerden topu oyuna sokmasıyla devam edecektir, bu durumda B takımının dip çizgisinden.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-4\nAçıklama: Hata, yanlış oyuncunun serbest atış ya da atışları atması halinde oluşursa, serbest atış ya da atışlar iptal edilecektir. Oyun henüz başlamamışsa, yönetilecek başka ihlal cezaları olmadıkça top, serbest atış çizgisi uzantısından oyuna sokması için rakiplere verilecektir. Eğer oyun devam etmişse, hatanın düzeltilmesi için oyun durdurulacaktır. Hatanın düzeltilmesinden sonra oyun, hatanın düzeltilmesi için oyunun durdurulduğu en yakın yerden devam e...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B takımı başantrenörünün teknik faulünden dolayı A2’nin kullandığı ilk serbest atış kurallara uygundur. Eğer başarılı olursa serbest atış geçerli sayılacaktır. A1’in yerine A2’nin attığı diğer 2 serbest atış iptal edilecektir. Oyun B takımı tarafından, geri sahasındaki serbest atış çizgisi uzantısından topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-4\nAçıklama: Hata, yanlış oyuncunun serbest atış ya da atışları atması halinde oluşursa, serbest atış ya da atışlar iptal edilecektir. Oyun henüz başlamamışsa, yönetilecek başka ihlal cezaları olmadıkça top, serbest atış çizgisi uzantısından oyuna sokması için rakiplere verilecektir. Eğer oyun devam etmişse, hatanın düzeltilmesi için oyun durdurulacaktır. Hatanın düzeltilmesinden sonra oyun, hatanın düzeltilmesi için oyunun durdurulduğu en yakın yerden devam e...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A2’nin 2 serbest atışı iptal edilecektir. Oyun B takımı tarafında, oyun saatinde 0.3 saniye ile geri sahasındaki serbest atış çizgisi uzantısında topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-4\nAçıklama: Hata, yanlış oyuncunun serbest atış ya da atışları atması halinde oluşursa, serbest atış ya da atışlar iptal edilecektir. Oyun henüz başlamamışsa, yönetilecek başka ihlal cezaları olmadıkça top, serbest atış çizgisi uzantısından oyuna sokması için rakiplere verilecektir. Eğer oyun devam etmişse, hatanın düzeltilmesi için oyun durdurulacaktır. Hatanın düzeltilmesinden sonra oyun, hatanın düzeltilmesi için oyunun durdurulduğu en yakın yerden devam e...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Hata hala düzeltilebilir. A2 tarafından kullanılan 2 serbest atış iptal edilecektir. Dördüncü çeyrek orta çizgi uzantısından pozisyon sırası hakkına göre başlayacaktır. (b) Hata artık düzeltilemez. Oyun devam edecektir.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-10\nAçıklama: Hata düzeltildikten sonra, yapılan düzeltme hak edilen serbest atış ya da atışların verilmesini içermediği sürece oyun, hatanın düzeltilmesi için durdurulduğu en yakın yerden devam edecektir. (a) Hata yapıldıktan sonra takım kontrolü değişmediyse oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir. (b) Hata yapıldıktan sonra takım kontrolü değişmediyse ve aynı takım sayı atarsa hata dikkate alınmayacaktır. Oyun, normal bir ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1, 2 serbest atış kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-10\nAçıklama: Hata düzeltildikten sonra, yapılan düzeltme hak edilen serbest atış ya da atışların verilmesini içermediği sürece oyun, hatanın düzeltilmesi için durdurulduğu en yakın yerden devam edecektir. (a) Hata yapıldıktan sonra takım kontrolü değişmediyse oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir. (b) Hata yapıldıktan sonra takım kontrolü değişmediyse ve aynı takım sayı atarsa hata dikkate alınmayacaktır. Oyun, normal bir ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Hata hala düzeltilebilir. A1, kimse dizilmeden 2 serbest atış kullanacaktır. İkinci çeyrek A takımı tarafından, pozisyon sırasına göre orta çizgi uzantısından topu oyuna sokmasıyla başlayacaktır.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-10\nAçıklama: Hata düzeltildikten sonra, yapılan düzeltme hak edilen serbest atış ya da atışların verilmesini içermediği sürece oyun, hatanın düzeltilmesi için durdurulduğu en yakın yerden devam edecektir. (a) Hata yapıldıktan sonra takım kontrolü değişmediyse oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir. (b) Hata yapıldıktan sonra takım kontrolü değişmediyse ve aynı takım sayı atarsa hata dikkate alınmayacaktır. Oyun, normal bir ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'A1 kimse dizilmeden 2 serbest atış kullanacaktır. Daha sonra A2, 2 serbest atış atacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-10\nAçıklama: Hata düzeltildikten sonra, yapılan düzeltme hak edilen serbest atış ya da atışların verilmesini içermediği sürece oyun, hatanın düzeltilmesi için durdurulduğu en yakın yerden devam edecektir. (a) Hata yapıldıktan sonra takım kontrolü değişmediyse oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir. (b) Hata yapıldıktan sonra takım kontrolü değişmediyse ve aynı takım sayı atarsa hata dikkate alınmayacaktır. Oyun, normal bir ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Hata dikkate alınmayacaktır. Oyun, herhangi bir başarılı sayı sonrasında olduğu gibi devam edecektir.',
                'choices': [
                    ('Hata dikkate alınmayacaktır. Oyun, herhangi bir başarılı sayı sonrasında olduğu gibi devam edecektir.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-10\nAçıklama: Hata düzeltildikten sonra, yapılan düzeltme hak edilen serbest atış ya da atışların verilmesini içermediği sürece oyun, hatanın düzeltilmesi için durdurulduğu en yakın yerden devam edecektir. (a) Hata yapıldıktan sonra takım kontrolü değişmediyse oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir. (b) Hata yapıldıktan sonra takım kontrolü değişmediyse ve aynı takım sayı atarsa hata dikkate alınmayacaktır. Oyun, normal bir ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Hata hala düzeltilebilir. A1, delegasyon üyesinden yardım aldığı için değiştirilmiştir ve oyun saati tekrar başlayıp durduğundan dolayı A1 tekrar oyuna girecek ve 2 serbest atış kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-10\nAçıklama: Hata düzeltildikten sonra, yapılan düzeltme hak edilen serbest atış ya da atışların verilmesini içermediği sürece oyun, hatanın düzeltilmesi için durdurulduğu en yakın yerden devam edecektir. (a) Hata yapıldıktan sonra takım kontrolü değişmediyse oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir. (b) Hata yapıldıktan sonra takım kontrolü değişmediyse ve aynı takım sayı atarsa hata dikkate alınmayacaktır. Oyun, normal bir ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Hata hala düzeltilebilir. A1, A takımına eşlik eden delegasyon üyesinden yardım aldığı için değiştirildiğinden ve oyun saati henüz başlamadığından dolayı A6, 2 serbest atış kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir.',
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'Madde 44 Düzeltilebilir hatalar | 44-17\nAçıklama: Maç saatindeki süreyle ilgili bir hata, başhakem müsabaka cetvelini imzalamadan önce herhangi bir zamanda hakemler tarafından düzeltilebilir.\nÖrnek 44-18: Dördüncü çeyrekte oyun saatinde 7 saniye kala ve skor A 76 - B 76 iken, A takımına ön sahasından topu oyuna sokma hakkı verilir. Top, oyun sahasındaki bir oyuncuya dokunduktan sonra oyun saati 3 saniye geç başlar. 4 saniye sonra A1 bir sahadan barılı bir sayı atar. Bu sırada hakemler, oyun saat...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Hakemler, A1'in şutunun kalan 7 saniyelik oyun süresi içinde atıldığını kabul ederse, A1'in sayısı geçerli olacaktır. Ayrıca hakemler, oyun saatinin 3 saniye geç başladığını kabul ederlerse, süre kalmamıştır. Hakemler oyunun bittiğine karar verir. B – Maç Kağıdı – Diskalifiye edici fauller",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'F-1 Tanım | F-1.3\nAçıklama: Maçtan önce başhakem, Anlık Tekrar Sistemi donanımını onaylayacak ve her iki başantrenöre de kullanılabilir olduğu konusunda bilgi verecektir. İnceleme için yalnızca başhakem tarafından onaylanan Anlık Tekrar Sistemi donanımını kullanılabilir.\nÖrnek F-1.2: A1’in sahadan sayı amacıyla şut girişimi başarılıdır, bu sırada oyun saati oyunun sonu için sesli işaretini verir. Onaylanmış bir Anlık Tekrar Sistemi donanımı mevcut değildir. B takımı menajeri, maçı takımının vide...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B takımı menajerinin Anlık Tekrar Sistemi incelemesi için takımının videosunu kullanma isteği reddedilecektir.',
                'choices': [
                    ('B takımı menajerinin Anlık Tekrar Sistemi incelemesi için takımının videosunu kullanma isteği reddedilecektir.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-2.1\nAçıklama: Bir çeyreğin veya uzatmanın sonunda Anında Tekrar Sistemi incelemesi olması durumunda hakemler her iki takımı da sahada tutacaktır. Çeyrekler veya uzatmadan önceki oyun arası ancak hakem nihai kararı bildirdikten sonra başlayacaktır.\nÖrnek F-2.2: A1’in sahadan bir şut girişimi başarılıdır. Yaklaşık olarak aynı anda oyun saati çeyreğin sonu için sesli işaret verir. Hakemler şutun oyun süresi içerisinde atılıp atılmadığından emin olamazlar ve Anlık Tekrar Sis...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Hakemler her iki takımı da oyun sahasında tutacaklardır. Oyun arası, hakem son kararını bildirdikten sonra başlayacaktır.',
                'choices': [
                    ('Hakemler her iki takımı da oyun sahasında tutacaklardır. Oyun arası, hakem son kararını bildirdikten sonra başlayacaktır.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "F-2 Genel prensipler | F-2.3\nAçıklama: Anlık Tekrar Sistemi incelemesi, incelenebilecek pozisyonu takip eden ilk fırsatta hakemler tarafından yapılır. Buna uygun durum, oyun saati durduğunda ve top öldüğünde yapılır. Ancak, başarılı bir sayıdan sonra hakemler oyunu durdurmazlarsa, Anlık Tekrar Sistemi incelemesi hakemlerin herhangi bir takımı dezavantajlı duruma düşürmeden oyunu durdurduğu ilk fırsatta yapılacaktır.\nÖrnek F-2.4: A1’in sahadan bir şut girişimi başarılıdır. Oyun, B1'in topu oyuna ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Anlık Tekrar Sistemi incelemesi amacıyla oyunu durdurmak için ilk fırsat, sayıdan sonra topun ölü olmasıdır. Oyun sırasında hakemlerin incelemeyi gerçekleştirmek için yeterli zamanları olmayabilir. Bu durumda hakemler hızlı hücum biter bitmez veya sayıdan sonra oyun ilk durduğu anda B takımını dezavantajlı duruma düşürmeden oyunu durduracaktır.',
                'choices': [
                    ('Anlık Tekrar Sistemi incelemesi amacıyla oyunu durdurmak için ilk fırsat, sayıdan sonra topun ölü olmasıdır. Oyun sırasında hakemlerin incelemeyi gerçekleştirm…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-2.6: A1’in sahadan bir şut girişimi başarılıdır. B takımı başantrenörü mola ister. Hakemler, A1'in şutunun 3 sayılık bölgeden atılıp atılmadığından emin değillerdir ve Anlık Tekrar Sistemi incelemesini kullanmaya karar verirler. İnceleme sırasında B takımı başantrenörü mola talebini iptal etmek ister.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'B takımının mola talebi, hakem kesin Anlık Tekrar Sistemi kararını bildirene kadar uygulanmayacaktır. Mola talebi, Anlık Tekrar Sistemi incelemesinin ardından, hakemin son kararını bildirmesi sonrasında iptal edilebilir. 1 EKİM 2020 – v.1.0 TÜRKİYE BASKETBOL FEDERASYONU 91',
                'choices': [
                    ('B takımının mola talebi, hakem kesin Anlık Tekrar Sistemi kararını bildirene kadar uygulanmayacaktır. Mola talebi, Anlık Tekrar Sistemi incelemesinin ardından,…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-2.7: B1’e bir sportmenlik dışı faul verilir. Hakemler, B1'in faulünün sportmenlik dışı olup olmadığından emin değillerdir. B6, B1 ile değişmek ister. İnceleme sırasında B6, takım sırasına geri döner.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'B6’nın oyuncu değişikliği talebi hakem kesin Anlık Tekrar Sistemi kararını bildirene kadar uygulanmayacaktır. Oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesinin ardından, hakemin son kararını bildirmesi sonrasında iptal edilebilir. F-3.1 Çeyreğin veya her uzatmanın sonunda',
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': "F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-3.1.1: Oyun saati çeyreğin sonu için sesli işaret verdiğinde A1’in sahadan bir şut girişimi başarılıdır. Hakemler, A1'in şutunun oyun süresinin bitiminden önce elden çıkıp çıkmadığından emin değillerdir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Anlık Tekrar Sistemi incelemesi çeyreğin sonunda, A1'in başarılı bir şutunun çeyreğin sonu için oyun saatinin sesli işaretinden önce elden çıkıp çıkmadığına karar vermek için kullanılabilir. Eğer inceleme, topun çeyrek için oyun süresinin bitiminden sonra atıldığını gösterirse, A1'in sayısı iptal edilecektir. Eğer inceleme, topun çeyrek için oyun süresinin bitiminden önce atıldığını gösterirse, başhakem A1'in sayısını başarılı olarak onaylayacaktır.",
                'choices': [
                    ("Anlık Tekrar Sistemi incelemesi çeyreğin sonunda, A1'in başarılı bir şutunun çeyreğin sonu için oyun saatinin sesli işaretinden önce elden çıkıp çıkmadığına ka…", True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': "F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-3.1.2: B takımı 2 sayı öndedir. Oyun saati ilk uzatmanın sonu için sesli işaret verdiğinde B1, A1'e faul yapar. Bu, B takımının dördüncü çeyrekteki beşinci takım faulüdür. Hakemler, B1’in faulünün ilk uzatmanın bitiminden önce olup olmadığından emin olmazlar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Anlık Tekrar Sistemi incelemesi her uzatmanın sonunda, B1’in faulünün oyun süresinin bitiminden önce olup olmadığına karar vermek için kullanılabilir. Eğer inceleme, B1'in faulünün oyun saati sesli işaretinden önce yapıldığını gösterirse, A1, 2 serbest kullanacaktır. Oyun herhangi bir son serbest atıştan sonra olduğu gibi, faulün yapıldığı anda oyun saatinde kalan süre ile devam edecektir. Eğer inceleme, B1'in faulünün oyun saati sesli işaretinden sonra meydana geldiğini ortaya koyarsa, yapılan faul sportmenlik dışı faul veya diskalifiye edici faul kriterlerini karşılamadığı ve ardından ikinci bir uzatma olmadığı sürece, B1'in faulü dikkate alınmayacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': "F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-3.1.3: Oyun saati ikinci uzatmanın sonu için sesli işaret verdiğinde B1, 2 sayılık başarısız şutunda A1'e faul yapar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Anlık Tekrar Sistemi incelemesi ikinci uzatmanın sonunda oyun saatinin, ikinci uzatmanın sonu için sesli işaretinden önce B1’in faulünün olup olmadığına karar vermek için kullanılabilir. Eğer inceleme, faulün ikinci uzatmanın bitiminden önce gerçekleştiğini gösterirse A1, 2 serbest atış kullanacaktır. Oyun herhangi bir son serbest atıştan sonra olduğu gibi, faulün yapıldığı anda oyun saatinde kalan süre ile devam edecektir. Eğer inceleme, B1'in faulünün oyun saati sesli işaretinden sonra meydana geldiğini ortaya koyarsa, yapılan faul sportmenlik dışı faul veya diskalifiye edici faul kriterlerini karşılamadığı ve ardından ikinci bir uzatma olmadığı sürece, B1'in faulü dikkate alınmayacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': "F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-3.1.4: Oyun saati çeyreğin sonu için sesli işaret verdiğinde A1’in sahadan 3 sayılık şut girişimi başarılıdır Hakemler, A1'in şutu sırasında sınır çizgisine temas edip etmediğinden emin değillerdir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Anlık Tekrar Sistemi incelemesi çeyreğin sonunda, A1'in başarılı bir şutunun, çeyreğin sonu için oyun saatinin sesli işaretinden önce elden çıkıp çıkmadığına karar vermek için kullanılabilir. Bu durumda inceleme ayrıca saha dışı bir ihlalinin olup olmadığına karar vermek için de kullanılabilir, eğer öyleyse ayrıca oyun saatinde ne kadar süre gösterileceği için de kullanılabilir.",
                'choices': [
                    ("Anlık Tekrar Sistemi incelemesi çeyreğin sonunda, A1'in başarılı bir şutunun, çeyreğin sonu için oyun saatinin sesli işaretinden önce elden çıkıp çıkmadığına k…", True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-3.1.5: Oyun saati çeyreğin sonu için sesli işaret verdiğinde A1’in sahadan 2 sayılık şut girişimi başarılıdır Hakemler, A takımı tarafından bir şut saati ihlali olup olmadığından emin değillerdir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi, çeyreğin sonunda, başarılı bir şutun çeyreğin sonu için oyun saatinin sesli işaretinde önce elden çıkıp çıkmadığına karar vermek için kullanılabilir. İnceleme ayrıca, A takımı tarafından bir şut saati ihlali olup olmadığına karar vermek için de kullanılabilir. Eğer inceleme A1'in sahadan attığı başarılı bir şutun, çeyreğin sonu için oyun saatinin sesli işaretinden 0.4 saniye önce elden çıktığını gösterirse ve eğer ayrıca inceleme A1'in başarılı şutundan 0.2 saniye önce şut saatinin sesli işaret verdiğinde topun A1’in ellerini terk etmediğini gösterirse A1’in atışı geçerli sayılmaz. Oyun B takımı tarafından, şut saati ihlalinin meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. B takımının oyun saatinde 0.6 saniyesi olacaktır. Şut saati kapatılacaktır.",
                'choices': [
                    ('Şut saati ihlali: Top B takımına verilir', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': "F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-3.1.6: Oyun saati ikinci çeyreğin sonu için sesli işaret verdiğinde A1’in sahadan bir şut girişimi başarılıdır. Hakemler, A1'in başarılı şutunun oyun saati çeyreğin sonu için sesli işaret vermeden önce elden çıkıp çıkmadığını, eğer öyleyse A takımının 8 saniye kuralını ihlal edip etmediğinden emin değiller...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Anlık Tekrar Sistemi incelemesi çeyreğin sonunda, A1'in başarılı bir şutunun çeyreğin sonu için oyun saatinin sesli işaretinde önce elden çıkıp çıkmadığına karar vermek için kullanılabilir. Anlık Tekrar Sistemi incelemesi ayrıca, A takımı tarafından bir 8 saniye ihlalinin olup olmadığına karar vermek için de kullanılabilir. Eğer inceleme, A1'in sahadan attığı başarılı bir şutun, çeyreğin sonu için oyun saatinin sesli işaretinden önce elden çıktığını gösterirse ve eğer ayrıca inceleme A1'in başarılı şutundan önce, A takımının oyun saati 3.4 saniye gösterdiğinde 8 saniye kuralını ihlal ettiğini gösteriyorsa A1’in sayısı geçerli sayılmaz. Oyun B takımı tarafında, 8 saniye ihlalinin meydana geldiği ön sahasındaki en yakın yerden topu oyuna sokmasıyla devam edecektir. B takımının oyun saatinde 3.4 saniyesi olacaktır. Şut saati kapatılacaktır. Eğer inceleme A takımının 8 saniye kuralını ihlal etmediğini gösterirse A1'in sayısı geçerli sayılacaktır. İkinci çeyrek sona ermiştir. İkinci devre, orta çizgi uzantısından pozisyon sırasına göre topun oyuna sokulmasıyla başlayacaktır.",
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': "F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-3.1.7: Oyun saatinde 2.5 saniye kala A1, sahadan bir şut girişiminde bulunur. Top çembere temas eder, B1 ribaundu alır ve dripling başlatır. Bu sırada oyun saati, oyunun sonu için sesli işaret verir. Hakemler, B1'in ribaund sonrasında topla oyun sahasına inerken saha dışına çıkıp çıkmadığından emin değille...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Anlık Tekrar Sistemi incelemesi, atış yapmayan bir oyuncunun saha dışı olup olmadığına karar vermek için kullanılamaz. F-3.2 Oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde',
                'choices': [
                    ('Anlık Tekrar Sistemi incelemesi, atış yapmayan bir oyuncunun saha dışı olup olmadığına karar vermek için kullanılamaz. F-3.2 Oyun saati dördüncü çeyrekte ve he…', True),
                    ('Anlık Tekrar Sistemi incelemesi, atış yapmayan bir oyuncunun saha dışı olup olmadığına karar vermek için kullanılabilir. F-3.2 Oyun saati dördüncü çeyrekte ve he…', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-3.2.1: Dördüncü çeyrekte oyun saatinde 1:41 kala şut saati sesli işaret verdiğinde A1’in sahadan bir şut girişimi başarılıdır. Şut saati sesli işaret verdiğinde hakemler, topun şut saati sesli işaretinden önce elden çıkıp çıkmadığından emin değiller. (a) başarılı bir sayı sonrasında B takımı tarafından top...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi oyun saati dördüncü çeyrekte 2:00 veya daha az gösterdiğinde, A1'in başarılı bir şutunun şut saati sesli işareti vermeden önce elden çıkıp çıkmadığına karar vermek için kullanılabilir. Hakemler sayı amacıyla sahadan yapılan başarılı bir atışın şut saatinin sesli işaretinden önce elden çıkıp çıkmadığına bakmak için top sepete girer girmez ve oyun saati durur durmaz oyunu derhal durdurmaya yetkilidirler. İnceleme en geç, hakemlerin oyunu ilk kez durdurmasının ardından top canlı hale gelene kadar yapılabilir. (a) hakemler oyunu derhal durduracak ve oyuna devam etmeden önce inceleme yapacaktır. (b) Hakemler incelemeyi, incelenebilecek pozisyonu için durum oluştuktan sonra herhangi bir nedenle oyunu durdurduklarında yapacaklardır. (c) İnceleme için belirlenen zaman süresi, hakemler tarafından oyun ilk kez durdurulduğunda top canlı olduğundan dolayı sona ermiştir. İlk verilen karar geçerliliğini korur. (a) veya (b)'de inceleme şut saati sesli işaretini verdiğinde topun hala A1'in ellerinde olduğunu gösteriyorsa bu bir şut saati ihlalidir. A1'in sayısı geçerli sayılmayacaktır. (a) oyun B takımı tarafından serbest atış çizgisi uzantısından topu oyuna sokmasıyla devam edecektir. (b) oyun topun kontrolüne sahip olan veya oyun durdurulduğunda topa sahip olma hakkı olan takımın topun bulunduğu en yakın yerden topu oyuna sokmasıyla veya varsa serbest atışlarla devam edecektir. (a) veya (b) inceleme şut saatinin sesli işaretinden önce topun A1'in başarılı bir atış için ellerini terk ettiğini belirtirse şut saati işareti göz ardı edilecektir. A1'in sayısı geçerli sayılacaktır. (a) oyun herhangi bir başarılı atış sonrasında olduğu gibi B takımının kendi dip çizgisinden topu oyuna sokmasıyla devam edecektir. (b) oyun topun kontrolüne sahip olan veya oyun durdurulduğunda topa sahip olma hakkı olan takımın topun bulunduğu en yakın yerden topu oyuna sokmasıyla veya varsa serbest atışlarla devam edecektir.",
                'choices': [
                    ('Şut saati ihlali: Top B takımına verilir', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-3.2.2: Dördüncü çeyrekte oyun saatinde 1:39 kala şut girişiminden uzak bir bölgede bir faul meydana geldiğinde A1 atış halindedir. (a) B2, A2’ye faul yapar. Bu çeyrekte üçüncü takım faulüdür. (b) B2, A2’ye faul yapar. Bu çeyrekte beşinci takım faulüdür. (c) A2, B2’ye faul yapar.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Oyun saati dördüncü çeyrekte 2:00 veya daha az gösterdiğine Anlık Tekrar Sistemi incelemesi aşağıdaki durumlara karar vermek için kullanılabilir. i. atış hali durumu şut girişiminde bulunan oyuncunun rakibine faul çalındığında başlamıştır; veya ii. şut girişiminde bulunan oyuncunun takım arkadaşına faul çalındığında top hala oyuncunun ellerindedir (a) Eğer inceleme A1'in atış halinde olmadığını gösterirse, top B2'nin faulü olduğunda ölü duruma gelir ve varsa sayı geçerli sayılmaz. İnceleme A1'in atış halinde olduğunu gösteriyorsa sayı olmuşsa geçerli sayılacaktır. Her iki durumda da oyun, A takımı tarafından B2'nin faulünün yapıldığı en yakın yerden topu oyuna sokmasıyla devam edecektir. (b) Eğer inceleme A1'in atış halinde olmadığını gösterirse, top B2'nin faulü olduğunda ölü duruma gelir ve varsa sayı geçerli sayılmaz. İnceleme A1'in atış halinde olduğunu gösteriyorsa sayı olmuşsa geçerli sayılacaktır. Her iki durumda da A2, B2'nin faulünün sonucu olarak 2 serbest atış kullanacaktır. Oyun herhangi bir son serbest atıştan sonra olduğu gibi devam edecektir. (c) Eğer inceleme topun şut atan oyuncunun ellerinden çıktığını gösteriyorsa, sayı olmuşsa geçerli sayılacaktır. Oyun A2'nin faulünün yapıldığı en yakın yerden B takımının topu oyuna sokmasıyla devam edecektir. İnceleme topun hala şut atan oyuncunun ellerinde olduğunu gösteriyorsa A2'nin faulü yapıldığında top ölü duruma gelir ve sayı olmuşsa geçerli sayılmayacak. Oyun B takımı tarafından serbest atış çizgisi uzantısından topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': "F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-3.2.3: Dördüncü çeyrekte oyun saatinde 1:37 kala şut saati sesli işaret verir. Yaklaşık olarak aynı anda, A1 ön sahasından bir sayı atar ve A2, A takımının ön sahasında toptan uzak bir bölgede B2'ye bir faul yapar. Bu, A takımının o çeyrekteki üçüncü takım faulüdür. Hakemler şut saati sesli işaret verdiğin...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Anlık Tekrar Sistemi incelemesi dördüncü çeyrekte oyun saati 2:00 veya daha az gösterdiğinde, şut saati sesli işaretini verdiğinde topun şut atan oyuncunun ellerinde olup olmadığına ve atış durumunun uzağındaki bir faulün ne zaman olduğuna karar vermek için kullanılabilir. (a) Eğer inceleme, şut saati sesli işaret vermeden evvel ve A2'nin faulü meydana gelmeden önce topun A1'in ellerini terk ettiğini gösterirse A2’nin faulü verilecektir ve A1’in sayısı geçerli sayılacaktır. Şut saati sesli işareti dikkate alınmayacaktır. (b) Eğer inceleme, A2'nin faulünün top A1'in ellerini terk etmeden ve şut saati sesli işaretini vermeden önce gerçekleştiğini gösterirse A2'nin faulü verilecektir ve A1'in sayısı geçerli sayılmayacaktır. Şut saati sesli işareti dikkate alınmayacaktır. (c) Eğer inceleme, top A1'in ellerini terk etmeden ve A2'nin faulü yapılmadan önce şut saati sesli işaret verirse bu, A takımı tarafından yapılan bir şut saati ihlalidir ve A2'nin faulü dikkate alınmayacaktır. A1'in sayısı geçerli sayılmayacaktır. (a) B2’nin faulünün meydana geldiği, ön sahasındaki en yakın yerden topu oyuna sokmasıyla devam edecektir. (b) ve (c) Oyun, B takımı tarafından kendi geri sahasındaki serbest atış çizgisi uzantısından topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Şut saati ihlali', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': "F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-3.2.4: Dördüncü çeyrekte oyun saatinde 1:37 kala şut saati sesli işaret verir. Yaklaşık olarak aynı anda, A1 ön sahasından bir sayı atar ve B2, A takımının ön sahasında toptan uzak bir bölgede A2'ye bir faul yapar. Bu, A takımının o çeyrekteki üçüncü takım faulüdür. Hakemler şut saati sesli işaret verdiğin...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Anlık Tekrar Sistemi incelemesi dördüncü çeyrekte oyun saati 2:00 veya daha az gösterdiğinde, şut saati sesli işaretini verdiğinde topun şut atan oyuncunun ellerinde olup olmadığına ve atış durumunun uzağındaki bir faulün ne zaman olduğuna karar vermek için kullanılabilir. Eğer inceleme, B2'nin faulünün şut saati sesli işaretini vermeden önce ve B2'nin faulünün A1 atış halindeyken yapıldığını ortaya koyarsa, B2'nin faulü verilecektir ve A1'in sayısı geçerli sayılacaktır. Şut saati sesli işareti dikkate alınmayacaktır. Oyun A takımı tarafından ön sahasında B2'nin faulünün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır. Eğer inceleme, top A1'in ellerini terk etmeden ve B2'nin faulü yapılmadan önce şut saati sesli işaretini verirse bu A takımı tarafından yapılan bir şut saati ihlalidir. B2'nin faulü dikkate alınmayacak ve A1'in sayısı geçerli sayılmayacak. Oyun, B takımı tarafından kendi geri sahasındaki serbest atış çizgisi uzantısından topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Şut saati ihlali: Top A takımına verilir', True),
                    ('Atış saati değişmez (devam eder)', False),
                    ('Atış saati 14 saniyeye ayarlanır', False),
                ]
            },
            {
                'text': "F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-3.2.5: Dördüncü çeyrekte oyun saatinde 1:39 kala B1, atış halinde olan A2'ye bir faul yapar. Yaklaşık olarak aynı anda şut girişiminden uzak bir bölgede B2, A2’ye faul yapar. Bu o çeyrekteki üçüncü takım faulüdür.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': "Anlık Tekrar Sistemi incelemesi dördüncü çeyrekte oyun saati 2:00 veya daha az gösterdiğinde B1’in faulü meydana geldiğinde atış halinin başlayıp başlamadığına ve şut girişiminden uzak bir bölgede B2’nin faulün ne zaman olduğuna karar vermek için kullanılabilir. Eğer inceleme B1’in faulünün önce olduğunu ve B2'nin faulü olduğunda A1'in atış halinde olmadığını gösterirse, top B1’in faulü olduğunda ölü duruma gelir varsa sayı geçerli sayılmaz. Oyun, A takımı tarafından B1'in faulünün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. B2'nin faulü top öldükten sonra meydana geldiği için sportmenlik dışı faul veya diskalifiye edici faul kriterlerini karşılamadığı sürece dikkate alınmayacaktır. Eğer inceleme B1’in faulünün önce olduğunu ve B1'nin faulü olduğunda A1'in atış halinde halinde olduğunu gösterirse varsa sayı geçerli sayılacaktır. A1, 1 serbest atış kullanacaktır. Sayı olmadıysa A1 2 veya 3 serbest atış kullanacaktır. Oyun herhangi bir son serbest atıştan sonra olduğu gibi devam edecektir. B2'nin faulü top öldükten sonra meydana geldiği için sportmenlik dışı faul veya diskalifiye edici faul kriterlerini karşılamadığı sürece, B2'nin faulü dikkate alınmayacaktır. Eğer inceleme B2’in faulünün önce olduğunu ve B1'nin faulü olduğunda A1'in atış halinde halinde olduğunu gösterirse varsa sayı geçerli sayılacaktır. B2'nin faulü, o çeyrekte B takımının üçüncü faulü ise oyun A takımı tarafından B2'nin faulünün meydana geldiği en yakın yerden topu oyuna sokmasıyla devam edecektir. B2'nin faulü, B takımının o çeyrekteki beşinci faulü ise A2, 2 serbest atış kullanacaktır. Oyun herhangi bir son serbest atıştan sonra olduğu gibi devam edecektir. B1'in faulü top öldükten sonra meydana geldiği için sportmenlik dışı faul veya diskalifiye edici faul kriterlerini karşılamadığı sürece, B1'in faulü dikkate alınmayacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': "F-2 Genel prensipler | F-2.5\nAçıklama: Bir mola veya oyuncu değişikliği talebi, Anlık Tekrar Sistemi incelemesi sona erdikten ve hakem son kararını bildirdikten sonra iptal edilebilir.\nÖrnek F-3.2.6: Dördüncü çeyrekte oyun saatinde 7.5 saniye kala ve ön sahasında topu oyuna sokan A1 topu elinden çıkarmadan hemen önce B1'e bir teknik faul verilir. Yaklaşık olarak aynı anda A2’ye yapmış olduğu temas nedeniyle başka bir hakem tarafından B2'ye sportmenlik dışı faul verilir. Hakemler, faullerin hangi...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'Anlık Tekrar Sistemi incelemesi meydana gelen faullerin sırasına karar vermek için kullanılamaz. Her iki faul de geçerli kalacaktır. Bir teknik faulün cezası önce yönetilecektir. Herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. A2 daha sonra 2 serbest atış kullanacaktır. Oyun A takımı tarafından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte 2:00 veya daha az gösterdiğinde sayıya yönelen top ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme topun sepete doğru inmekte olduğunu gösterirse, sayıya yönelen top ihlali geçerli kalacaktır. Eğer inceleme topun henüz sepete doğru inmediğini gösterirse, ihlal kararı geri alınacak ve bir hava atışı durumu oluşacaktır. Eğer inceleme topun henüz sepete doğru inmekte olmadığını gösterirse, sayıya yönelen top ihlali kararı iptal edilecektir. Top sepete girmediği için; • topun hemen ve açık bir şekilde kontrolünü ele geçiren takım, oyun durdurulduğu anda topun bulunduğu en yakın yerden topu oyuna sokma hakkına sahip olacaktır. • eğer hiçbir takım topun kontrolünü hemen ve açık bir şekilde kazanamazsa, bir hava atışı durumu oluşur. Topun oyuna sokulması A takımı tarafından yapılacaksa, şut saati oyun durdurulduğunda kalan süre kadar zamanı gösterecektir. Topun oyuna sokulması B takımı tarafından kendi geri sahasından yapılacaksa B takımının şut saatinde 24 saniyesi olacaktır. Ön sahasındaysa, B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Top sepetten içeri girdiğinden, müdahale ihlali kararını incelemeye gerek yoktur. Sayı geçerli sayılacaktır. Oyun, şut saatinde 24 saniye ile B takımı tarafından kendi dip çizginin gerisinden topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi, B1 veya A1 tarafından yapılan sayıya yönelen top ihlali meydana gelmediğini gösterir. Bundan başka inceleme, B2'nin veya A2'nin aksama müdahale ihlalinin meydana geldiğini gösterir. Aksama müdahale ihlali cezası uygulanır. (a) İhlali B2 yaptıysa sayı geçerli sayılacaktır. Oyun, şut saatinde 24 saniye ile B takımı tarafından kendi dip çizginin gerisinden topu oyuna sokmasıyla devam edecektir. (b) İhlali A2 yaptıysa sayı geçerli sayılmayacaktır Oyun, şut saatinde 24 saniye ile B takımı tarafından serbest atış çizgisi uzantısından topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi, aksama müdahale ihlalinin meydana gelmediğini gösterir. Her iki durumda da topun hemen ve açık bir şekilde kontrolünü kazanan takım, oyun durdurulduğunda topun bulunduğu en yakın yerden topu oyuna sokma hakkına sahip olacaktır. Topun oyuna sokulma hakkı A takımına verilirse, o takımın şut saatinde kalan süresi kadar zamanı olacaktır. Eğer B takımına verilirse şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi, aksama müdahale ihlalinin meydana gelmediğini gösterir. Her iki durumda da topun hemen ve açık bir şekilde kontrolünü kazanan takım, oyun durdurulduğunda topun bulunduğu en yakın yerden topu oyuna sokma hakkına sahip olacaktır. Topun oyuna sokulma hakkı A takımına verilirse, o takımın şut saatinde 14 saniyesi olacaktır. Eğer B takımına verilirse şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi, aksama müdahale ihlalinin meydana gelmediğini gösterir. Her iki durumda da topun saha dışına çıkmasına neden olmayan takıma topu oyuna sokma hakkı verilecektir. Topun oyuna sokulma hakkı A takımına verilirse, o takımın şut saatinde kalan süresi kadar zamanı olacaktır. Eğer B takımına verilirse şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi, sayıya yönelen topa müdahale ihlalinin meydana gelmediğini gösterir. Her iki durumda da hiçbir takım hemen ve açık olarak bir kontrol sağlayamamıştır. Bu bir hava atışı durumudur. Topun oyuna sokulma hakkı A takımına verilirse, o takımın şut saatinde kalan süresi kadar zamanı olacaktır. Topun oyuna sokulma hakkı kendi geri sahasından B takımına verilirse, B takımının şut saatinde 24 saniyesi olacaktır. Ön sahasındaysa, B takımının şut saatinde 14 saniyesi olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi, aksama müdahale ihlalinin meydana gelmediğini gösterir. Her iki durumda da, B2 veya A2'ye yapılan faulün cezası uygulanacaktır.",
                'choices': [
                    ("Anlık Tekrar Sistemi incelemesi, aksama müdahale ihlalinin meydana gelmediğini gösterir. Her iki durumda da, B2 veya A2'ye yapılan faulün cezası uygulanacaktır.", True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi, sayıya yönelen topa müdahale ihlalinin meydana geldiğini gösterir. Her iki durumda da, top öldükten sonra meydana geldiği için sportmenlik dışı faul veya diskalifiye edici faul olarak değerlendirilmediği sürece, B2 veya A2'ye yapılan faul dikkate alınmayacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi sadece, hakemler tarafından sayıya yönelen top ihlali çalındığında kullanılabilir.',
                'choices': [
                    ('Anlık Tekrar Sistemi incelemesi sadece, hakemler tarafından sayıya yönelen top ihlali çalındığında kullanılabilir.', True),
                    ('Anlık Tekrar Sistemi incelemesi sadece, hakemler tarafından sayıya yönelen top ihlali çalındığında kullanılamaz.', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi sadece, hakemler tarafından sayıya yönelen top ihlali çalındığında kullanılabilir.',
                'choices': [
                    ('Anlık Tekrar Sistemi incelemesi sadece, hakemler tarafından sayıya yönelen top ihlali çalındığında kullanılabilir.', True),
                    ('Anlık Tekrar Sistemi incelemesi sadece, hakemler tarafından sayıya yönelen top ihlali çalındığında kullanılamaz.', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi, dördüncü çeyrekte oyun saati 2:00 veya daha az gösterdiğinde, B2’nin sayıya yönelen top ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme, B2'nin sepetin içine, aşağıya doğru giden topa temas ettiğini gösterirse sayıya yönelen top ihlali geçerliliğini koruyacaktır. A1'e 2 sayı verilecektir. A1 ayrıca 1 serbest atış kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir. Eğer inceleme, B2'nin yukarıya doğru giden topa temas ettiğini gösterirse sayıya yönelen top ihlal kararı iptal edilecektir. A1, 2 serbest atış kullanacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir.",
                'choices': [
                    ('1 serbest atış', True),
                    ('0 serbest atış', False),
                    ('2 serbest atış', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi, dördüncü çeyrekte oyun saati 2:00 veya daha az gösterdiğinde, topun saha dışına çıkmasına neden olan oyuncuyu belirlemek için kullanılabilir. Mola süresi inceleme sona erene ve hakem son kararını bildirene kadar başlamayacaktır.',
                'choices': [
                    ('Anlık Tekrar Sistemi incelemesi, dördüncü çeyrekte oyun saati 2:00 veya daha az gösterdiğinde, topun saha dışına çıkmasına neden olan oyuncuyu belirlemek için …', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi yalnızca dördüncü çeyrekte oyun saati 2:00 veya daha az gösterdiğinde topun saha dışına çıkmasına neden olan oyuncuyu belirlemek için kullanılabilir.',
                'choices': [
                    ('Anlık Tekrar Sistemi incelemesi yalnızca dördüncü çeyrekte oyun saati 2:00 veya daha az gösterdiğinde topun saha dışına çıkmasına neden olan oyuncuyu belirleme…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi, atış yapmayan bir oyuncunun saha dışında olup olmadığına karar vermek için kullanılamaz. F-3.3 Oyunun herhangi bir anında',
                'choices': [
                    ('Anlık Tekrar Sistemi incelemesi, atış yapmayan bir oyuncunun saha dışında olup olmadığına karar vermek için kullanılamaz. F-3.3 Oyunun herhangi bir anında', True),
                    ('Anlık Tekrar Sistemi incelemesi, atış yapmayan bir oyuncunun saha dışında olup olmadığına karar vermek için kullanılabilir. F-3.3 Oyunun herhangi bir anında', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında faul yapıldığında A1’in atış halinde olup olmadığına karar vermek için kullanılamaz.',
                'choices': [
                    ('Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında faul yapıldığında A1’in atış halinde olup olmadığına karar vermek için kullanılamaz.', True),
                    ('Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında faul yapıldığında A1’in atış halinde olup olmadığına karar vermek için kullanılabilir.', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında, A1’in başarılı atışının 2 ya da 3 sayı olarak sayılıp sayılmayacağına karar vermek için kullanılabilir. İnceleme oyun saati durduğunda ve topun öldüğü ilk fırsatta yapılacaktır. Ancak hakemler, oyunu herhangi bir nedenle derhal durdurmaya yetkilidirler. (a) hakemler oyunu derhal durduracak ve top canlanmadan önce incelemeyi yapacaklardır. (b) hakemler oyunu derhal durduracak ve her iki takımı da dezavantajlı duruma düşürmeden incelemeyi yapacaklardır. İnceleme, hakemlerin oyunu herhangi bir nedenle ilk kez durdurmasından sonra ve top yeniden canlanmadan önce yapılmalıdır. Bu durum dördüncü çeyreğin son 2 dakikası veya uzatmalar için de geçerlidir. (c) Mola verilmeden önce inceleme gerçekleştirilecektir. İncelemenin sonunda kesin kararının verilmesinden sonra, başantrenörün mola talebini geri çekmemesi halinde mola başlayacaktır. Bütün durumlarda, son kararın bildirilmesinden ve (c) şıkkındaki molanın ardından oyun, başarılı bir sayıdan sonra olduğu gibi B takımı tarafından kendi dip çizgisinin gerisinden topu oyuna sokmasıyla devam edecektir.',
                'choices': [
                    ('Top ilgili takıma verilir (oyuna sokma)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında, A1’in başarılı atışının 2 ya da 3 sayı olarak sayılıp sayılmayacağına karar vermek için kullanılabilir. İnceleme oyun saati durduğunda ve topun öldüğü ilk fırsatta yapılacaktır. Ancak hakemler, oyunu herhangi bir nedenle derhal durdurmaya yetkilidirler. Hakemler A2'nin faulü nedeniyle oyunu başarılı sayıdan sonra ilk kez durdurulduğundan dolayı bu anda incelemeyi gerçekleştireceklerdir. Son kararın bildirilmesinden sonra oyun, B2'nin serbest atış ya da atışları ile devam edecektir.",
                'choices': [
                    ('Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında, A1’in başarılı atışının 2 ya da 3 sayı olarak sayılıp sayılmayacağına karar vermek için kullanılabi…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesini kullanma süresi, topun B2'nin ilk veya tek serbest atışı için canlanmasıyla sona erer. İlk verilen karar geçerliliğini korur.",
                'choices': [
                    ("Anlık Tekrar Sistemi incelemesini kullanma süresi, topun B2'nin ilk veya tek serbest atışı için canlanmasıyla sona erer. İlk verilen karar geçerliliğini korur.", True),
                    ('1 serbest atış', False),
                    ('0 serbest atış', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında, sayı amacıyla şut atan oyuncuya 2 ya da 3 serbest atış hakkı verilip verilmeyeceğine karar vermek için kullanılabilir. İnceleme, ilk serbest atış için top canlanmadan önce yapılacaktır.',
                'choices': [
                    ('3 serbest atış', True),
                    ('2 serbest atış', False),
                    ('1 serbest atış', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında, B2'nin sportmenlik dışı faulünün kişisel faul olarak indirilip indirilmeyeceğine karar vermek için kullanılabilir. İnceleme faulün sportmenlik dışı faul kriterlerini karşıladığını gösterirse B2'nin faulü sportmenlik dışı olarak kalacaktır. İncelemesi faulün sportmenlik dışı faul kriterlerini karşılamadığını gösterirse B2'nin faulü kişisel faul olarak indirilecektir. Bu bir topun oyuna sokulması faulüdür.",
                'choices': [
                    ('Kişisel faul', True),
                    ('Faul yok / oyun devam', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında kişisel, sportmenlik dışı veya diskalifiye edici faulün bir teknik faul olarak kabul edilip edilmeyeceğine karar vermek için kullanılabilir. İnceleme B1’in dirseğini savurması sonucu A1'e temas etmediğini gösterirse, B1'in faulü teknik faul olarak değiştirilecektir.",
                'choices': [
                    ('Oyuncu değişikliği yapılır', True),
                    ('Oyuncu değişikliğine izin verilmez', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında, kişisel faulün bir sportmenlik dışı faul olarak yükseltilip yükseltilmeyeceğine karar vermek için kullanılabilir. Ancak incelemede hiçbir şekilde bir temas olmadığını gösterirse kişisel faul iptal edilemez.',
                'choices': [
                    ('Kişisel faul', True),
                    ('Faul yok / oyun devam', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında, bir sportmenlik dışı faulün kişisel faul olarak indirilmesi veya diskalifiye edici bir faul olarak yükseltilmesi konusunda karar vermek için kullanılabilir. Ancak inceleme A1'in, B1'in koluna vurarak temastan sorumlu olduğunu gösterirse B1'in sportmenlik dışı savunma faulü kişisel faul olarak düşürülür fakat, A1'in hücum faulü olarak değiştirilemez ve iptal edilemez.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında, kişisel faulün sportmenlik dışı bir faul olarak yükseltilip yükseltilmeyeceğine karar vermek için kullanılabilir. Ancak inceleme A1'in, B1'e şarj ederek temastan sorumlu olduğunu gösterirse, B1'in savunma , A1'in hücum faulü olarak değiştirilemez ve iptal edilemez.",
                'choices': [
                    ('Kişisel faul', True),
                    ('Faul yok / oyun devam', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında, sportmenlik dışı faulün bir kişisel faul olarak indirilmesi veya diskalifiye edici bir faul olarak yükseltilmesi konusunda karar vermek için kullanılabilir. İnceleme B1'in faulünün sportmenlik dışı bir faul olduğunu gösterirse faul, sportmenlik dışı olarak kalacaktır. İnceleme B1'in faulünün bir kişisel faul olduğunu gösterirse faul, yürüme ihlalinden sonra olduğu için dikkate alınmayacaktır.",
                'choices': [
                    ('Yürüme ihlali (top kaybı)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında, sportmenlik dışı faulün bir kişisel faul olarak indirilmesine ya da bir diskalifiye edici faul olarak yükseltilip yükseltilmeyeceğine karar vermek için kullanılabilir. İnceleme B2'nin faulünün bir sportmenlik dışı faul olduğunu gösterirse, faul sportmenlik dışı olarak kalacaktır. A1, B1'in kişisel faulünden dolayı kimse dizilmeden 2 serbest atış kullanacaktır. A1, B2'nin sportmenlik dışı faulünden dolayı kimse dizilmeden 2 serbest atış daha kullanacaktır. Oyun A takımı tarafından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır. İnceleme B2'nin faulünün bir kişisel faul olduğunu gösterirse, ilk faulden sonra olduğu için dikkate alınmayacaktır. A1, B1'in faulünden dolayı 2 serbest atış atacaktır. Oyun, herhangi bir son serbest atış sonrasında olduğu gibi devam edecektir.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Eğer inceleme B1'in, A1'e yaptığı faulün bir sportmenlik dışı faul olduğunu gösterirse B1, ikinci sportmenlik dışı faulünden dolayı otomatik olarak diskalifiye edilecektir. B1’in teknik faulü dikkate alınmayacak ve ne kendisine ne de B takımının başantrenörüne verilmeyecektir. A1, B1'in sportmenlik dışı faulünden dolayı kimse dizilmeden 1 serbest atış kullanacaktır. Oyun A takımı tarafından, ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Oyun hemen durdurulacaktır. Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında, her iki saatte ne kadar süre gösterileceğine karar vermek için kullanılabilir. İncelemeden sonra oyun A takımı tarafından, oyun durdurulduğunda topun bulunduğu en yakın yerden topu oyuna sokmasıyla devam edecektir. A takımının oyun saati ve şut saatinde kalan süresi kadar zamanı olacaktır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında, hatanın ardından oyun saati çalışmaya başladıktan sonra ilk ölü topun ardından, top canlanmadan önce doğru serbest atışı kullanması gereken oyuncuyu belirlemek için kullanılabilir. İnceleme sonucunda, yanlış bir oyuncunun serbest atış ya da atışları kullandığı tespit edilirse, yanlış oyuncunun serbest atış ya da atışları atmasına izin verilen düzeltilebilir bir hata durumu oluşmuştur. A2’nin serbest atış ya da atışları, başarılı olup olmadığına bakılmaksızın iptal edilecektir. Oyun B takımı tarafından, geri sahasındaki serbest atış çizgisi uzantısından topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 24 saniyesi olacaktır.',
                'choices': [
                    ('İzin verilir', True),
                    ('izin verilmez', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Düzen yeniden sağlandıktan sonra hakemler Anlık Tekrar Sistemi incelemesini oyunun herhangi bir anında, herhangi bir şiddet eylemi sırasında diğer oyuncuların ve takım sıralarında oturmasına izin verilen tüm kişilerin kavgaya katılımını belirlemek için kullanabilirler. Kavganın açık ve kesin kanıtlarını topladıktan sonra başhakem son kararını hakem masası önünde bildirecek ve her iki başantrenörü de bilgilendirecektir.',
                'choices': [
                    ('İzin verilir', True),
                    ('izin verilmez', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Düzen yeniden sağlandıktan sonra hakemler Anlık Tekrar Sistemi incelemesini oyunun herhangi bir anında, herhangi bir şiddet eylemi sırasında oyuncuların katılımını belirlemek için kullanabilirler. Kavganın açık ve kesin kanıtlarını topladıktan sonra başhakem son kararını hakem masası önünde bildirecek ve her iki başantrenörü de bilgilendirecektir.',
                'choices': [
                    ('Düzen yeniden sağlandıktan sonra hakemler Anlık Tekrar Sistemi incelemesini oyunun herhangi bir anında, herhangi bir şiddet eylemi sırasında oyuncuların katılı…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.2.7\nAçıklama: Anlık Tekrar Sistemi incelemesi, oyun saati dördüncü çeyrekte ve her uzatmada 2:00 veya daha az gösterdiğinde sayıya yönelen top veya müdahale ihlalinin doğru çalınıp çalınmadığına karar vermek için kullanılabilir. Eğer inceleme sayıya yönelen top veya müdahale ihlalinin yanlış çalındığını gösterirse oyun aşağıdaki şekilde devam edecektir. Eğer karardan sonra; • top kurallara uygun olarak sepetten içeri girdiyse sayı geçerli olacak ve yeni hücum takımı ke...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi incelemesi oyun sırasında herhangi bir zamanda oyuncuların herhangi bir şiddet eylemine katılıp katılmadıklarını belirlemek için kullanılabilir. Hakemler faulü hakem masasına bildirmeden önce incelemeyi yapabilirler. İncelemede şiddet eylemlerinin gerçekleştiği tespit edilirse, hakem B1'in faulünü ve ardından şiddet eylemini bildirecek ve oyun verilecek cezalarla devam edecektir.",
                'choices': [
                    ('Anlık Tekrar Sistemi incelemesi oyun sırasında herhangi bir zamanda oyuncuların herhangi bir şiddet eylemine katılıp katılmadıklarını belirlemek için kullanıla…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.3.19\nAçıklama: Anında/direkt olarak çalınmayan bir şiddet eyleminin meydana geldiği durumlarda hakemler, herhangi olası bir şiddet eylemi veya potansiyel şiddet eylemi için inceleme yapmak amacıyla oyunu herhangi bir zamanda durdurmaya yetkilidirler. Hakemler, Anlık Tekrar Sistemi incelemesi ihtiyacını belirlemeli ve inceleme, hakemler oyunu ilk kez durdurduğunda yapılmalıdır. İncelemesi bir şiddet eylemi gerçekleştiğini belirtirse, hakemler ihlali bildirecek ve şiddet...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Her iki durumda da Anlık Tekrar Sistemi incelemesi oyun sırasında herhangi bir zamanda takım üyelerinin herhangi bir şiddet eylemine katılımını belirlemek için kullanılabilir. Hakemler, her iki takımı da dezavantajlı duruma sokmadan oyunu derhal durdurmaya yetkilidir veya inceleme için oyunun durdurulmasını kullanabilirler. İnceleme A2'nin B2'ye dirseğiyle vurduğunu gösterirse hakemler A2'ye sportmenlik dışı faul verebilir. B2, kimse dizilmeden 2 serbest atış kullanacaktır. İçinde (a) oyun, B takımının ön sahasındaki oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır. (b) oyun, B takımının saha dışı ihlalinin gerçekleştiği en yakın yerden A takımının topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde kalan süresi olacaktır.",
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.3.19\nAçıklama: Anında/direkt olarak çalınmayan bir şiddet eyleminin meydana geldiği durumlarda hakemler, herhangi olası bir şiddet eylemi veya potansiyel şiddet eylemi için inceleme yapmak amacıyla oyunu herhangi bir zamanda durdurmaya yetkilidirler. Hakemler, Anlık Tekrar Sistemi incelemesi ihtiyacını belirlemeli ve inceleme, hakemler oyunu ilk kez durdurduğunda yapılmalıdır. İncelemesi bir şiddet eylemi gerçekleştiğini belirtirse, hakemler ihlali bildirecek ve şiddet...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Her iki durumda da Anlık Tekrar Sistemi oyun sırasında herhangi bir zamanda, herhangi bir şiddet eylemi sırasında takım üyelerinin katılımını belirlemek için kullanılabilir. Top sepette içeri girdiğinde hakemler oyunu durduracaklardır. Anlık Tekrar Sistemi incelemesi B1'in faulünden önce A1'in dirseğiyle B1'e vurduğunu gösterir. Hakemler A1’e sportmenlik dışı faul verebilirler. Cezalar, faullerin meydana geldiği sıraya göre uygulanacaktır. (a) A1’in sayısı geçerli sayılmayacaktır. A1’in sportmenlik dışı faulünden dolayı B1 kimse dizilmeden 2 serbest atış kullanacaktır. Oyun, B takımı tarafından ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır. (b) A1’in sayısı geçerli sayılacaktır. A1’in sportmenlik dışı faulünden dolayı B1 kimse dizilmeden 2 serbest atış kullanacaktır. Daha sonra A1, kimse dizilmeden B1'in kişisel faulü için 1 serbest atış kullanacaktır. Oyun herhangi bir son serbest atıştan sonra olduğu gibi devam edecektir. B1'in faulünün cezası, A1'in sportmenlik dışı faulünün cezasının bir parçası olarak önceki topa sahip olma hakkını iptal eder.",
                'choices': [
                    ('Kişisel faul', True),
                    ('Faul yok / oyun devam', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.3.19\nAçıklama: Anında/direkt olarak çalınmayan bir şiddet eyleminin meydana geldiği durumlarda hakemler, herhangi olası bir şiddet eylemi veya potansiyel şiddet eylemi için inceleme yapmak amacıyla oyunu herhangi bir zamanda durdurmaya yetkilidirler. Hakemler, Anlık Tekrar Sistemi incelemesi ihtiyacını belirlemeli ve inceleme, hakemler oyunu ilk kez durdurduğunda yapılmalıdır. İncelemesi bir şiddet eylemi gerçekleştiğini belirtirse, hakemler ihlali bildirecek ve şiddet...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi oyun sırasında herhangi bir zamanda, herhangi bir şiddet eylemi sırasında takım üyelerinin katılımını belirlemek için kullanılabilir. İnceleme A2'nin B2'ye dirseğiyle vurduğunu gösterirse hakemler A2'ye sportmenlik dışı faul verebilir. Cezalar faullerin oluş sırasına göre uygulanacaktır. B2, kimse dizilmeden 2 serbest atış kullanacaktır. Oyun, B3'ün faulünün olduğu en yakın yerden A takımının topu oyuna sokmasıyla devam edecektir. Eğer topun oyuna sokulması; (a) Geri sahadan olursa şut saatinde 24 saniyesi olacaktır. (b) ön sahadan olursa şut saati 14 saniye veya daha fazla gösteriyorsa şut saatinde kalan süreyle, şut saati13 saniye veya daha az gösteriyorsa şut saatinde14 saniyeyle. B3'ün faulünün cezası, A2'nin sportmenlik dışı faulünün cezasının bir parçası olarak B takımının önceki topa sahip olma hakkını iptal eder.",
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.3.19\nAçıklama: Anında/direkt olarak çalınmayan bir şiddet eyleminin meydana geldiği durumlarda hakemler, herhangi olası bir şiddet eylemi veya potansiyel şiddet eylemi için inceleme yapmak amacıyla oyunu herhangi bir zamanda durdurmaya yetkilidirler. Hakemler, Anlık Tekrar Sistemi incelemesi ihtiyacını belirlemeli ve inceleme, hakemler oyunu ilk kez durdurduğunda yapılmalıdır. İncelemesi bir şiddet eylemi gerçekleştiğini belirtirse, hakemler ihlali bildirecek ve şiddet...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi oyun sırasında herhangi bir zamanda, herhangi bir şiddet eylemi sırasında ekip üyelerinin katılımını belirlemek için kullanılabilir. Eğer inceleme A2'nin B2'ye dirseğiyle vurduğunu tespit ederse hakemler A2’ye sportmenlik dışı faul verebilirler. Cezalar, faullerin meydana geldiği sıraya göre uygulanacaktır. B2 kimse dizilmeden 2 serbest atış kullanacaktır. Ardından A1, 2 serbest atış kullanacaktır. Oyun, herhangi bir son serbest atıştan sonra olduğu gibi devam edecektir. B3'ün faulünün cezası, A2'nin sportmenlik dışı faulünün bir parçası olarak B takımının önceki topa sahip olma hakkını iptal eder.",
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.3.19\nAçıklama: Anında/direkt olarak çalınmayan bir şiddet eyleminin meydana geldiği durumlarda hakemler, herhangi olası bir şiddet eylemi veya potansiyel şiddet eylemi için inceleme yapmak amacıyla oyunu herhangi bir zamanda durdurmaya yetkilidirler. Hakemler, Anlık Tekrar Sistemi incelemesi ihtiyacını belirlemeli ve inceleme, hakemler oyunu ilk kez durdurduğunda yapılmalıdır. İncelemesi bir şiddet eylemi gerçekleştiğini belirtirse, hakemler ihlali bildirecek ve şiddet...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi oyun sırasında herhangi bir zamanda, herhangi bir şiddet eylemi sırasında takım üyelerinin katılımını belirlemek için kullanılabilir. İnceleme A2'nin B2'ye dirseğiyle vurduğunu gösterirse, hakemler A2'ye sportmenlik dışı faul verebilir. Cezalar faullerin oluş sırasına göre uygulanacaktır. B2, diziliş olmadan 2 serbest atış atacaktır. Oyun, A1'in faulünün olduğu en yakın yerden B takımının topu oyuna sokmasıyla devam edecektir. Eğer topun oyuna sokulması; (a) Geri sahadan olursa şut saatinde 24 saniyesi olacaktır. (b) ön sahadan olursa şut saati 14 saniyesi olacaktır. A1'in faulünün cezası, A2'nin sportmenlik dışı faulünün cezasının bir parçası olarak B takımının önceki topa sahip olma hakkını iptal eder.",
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.3.19\nAçıklama: Anında/direkt olarak çalınmayan bir şiddet eyleminin meydana geldiği durumlarda hakemler, herhangi olası bir şiddet eylemi veya potansiyel şiddet eylemi için inceleme yapmak amacıyla oyunu herhangi bir zamanda durdurmaya yetkilidirler. Hakemler, Anlık Tekrar Sistemi incelemesi ihtiyacını belirlemeli ve inceleme, hakemler oyunu ilk kez durdurduğunda yapılmalıdır. İncelemesi bir şiddet eylemi gerçekleştiğini belirtirse, hakemler ihlali bildirecek ve şiddet...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi oyun sırasında herhangi bir zamanda, herhangi bir şiddet eylemi sırasında takım üyelerinin katılımını belirlemek için kullanılabilir. İnceleme A1'in B1'e dirseğiyle vurduğunu gösterirse hakemler A1'e sportmenlik dışı faul verebilir. Her iki sportmenlik dışı faul de aynı duran saati periyodunda periyotta meydana gelmiştir. Her iki eşit ağırlıklı sportmenlik dışı faul cezaları birbirini iptal edecektir. Oyun A1'in faulünün olduğu en yakın yerden A takımının topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde kalan süresi olacaktır.",
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.3.19\nAçıklama: Anında/direkt olarak çalınmayan bir şiddet eyleminin meydana geldiği durumlarda hakemler, herhangi olası bir şiddet eylemi veya potansiyel şiddet eylemi için inceleme yapmak amacıyla oyunu herhangi bir zamanda durdurmaya yetkilidirler. Hakemler, Anlık Tekrar Sistemi incelemesi ihtiyacını belirlemeli ve inceleme, hakemler oyunu ilk kez durdurduğunda yapılmalıdır. İncelemesi bir şiddet eylemi gerçekleştiğini belirtirse, hakemler ihlali bildirecek ve şiddet...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi oyun sırasında herhangi bir zamanda, herhangi bir şiddet eylemi sırasında takım üyelerinin katılımını belirlemek için kullanılabilir. İnceleme A1'in B1'e dirseğiyle vurduğunu gösterirse hakemler A1'e sportmenlik dışı faul verebilir. Her iki sportmenlik dışı faul de aynı duran saati periyodunda periyotta meydana gelmiştir. Cezalar ihlalin meydana geldiği sıraya göre uygulanacaktır. B1 kimse dizilmeden 2 serbest atış kullanacaktır. Daha sonra A1 kimse dizilmeden 3 serbest atış kullanacaktır. Oyun A takımının ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. A takımının şut saatinde 14 saniyesi olacaktır. A takımının topa sahip olma hakkı sırası, B takımının önceki topa sahip olma hakkını iptal eder.",
                'choices': [
                    ('2 serbest atış', True),
                    ('1 serbest atış', False),
                    ('3 serbest atış', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.3.19\nAçıklama: Anında/direkt olarak çalınmayan bir şiddet eyleminin meydana geldiği durumlarda hakemler, herhangi olası bir şiddet eylemi veya potansiyel şiddet eylemi için inceleme yapmak amacıyla oyunu herhangi bir zamanda durdurmaya yetkilidirler. Hakemler, Anlık Tekrar Sistemi incelemesi ihtiyacını belirlemeli ve inceleme, hakemler oyunu ilk kez durdurduğunda yapılmalıdır. İncelemesi bir şiddet eylemi gerçekleştiğini belirtirse, hakemler ihlali bildirecek ve şiddet...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi oyun sırasında herhangi bir zamanda, herhangi bir şiddet eylemi sırasında takım üyelerinin katılımını belirlemek için kullanılabilir. İnceleme A1'in B1'e dirseğiyle vurduğunu gösterirse hakemler A1'e sportmenlik dışı faul verebilir. Her iki sportmenlik dışı faul de aynı duran saati periyodunda periyotta meydana gelmiştir. A1’in sayısı geçerli sayılacaktır. Her iki eşit ağırlıklı sportmenlik dışı faul cezaları birbirini iptal edecektir. Oyun başarılı bir sayı sonrasında olduğu gibi B takımının dip çizgisinin gerisinden topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.3.19\nAçıklama: Anında/direkt olarak çalınmayan bir şiddet eyleminin meydana geldiği durumlarda hakemler, herhangi olası bir şiddet eylemi veya potansiyel şiddet eylemi için inceleme yapmak amacıyla oyunu herhangi bir zamanda durdurmaya yetkilidirler. Hakemler, Anlık Tekrar Sistemi incelemesi ihtiyacını belirlemeli ve inceleme, hakemler oyunu ilk kez durdurduğunda yapılmalıdır. İncelemesi bir şiddet eylemi gerçekleştiğini belirtirse, hakemler ihlali bildirecek ve şiddet...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi oyun sırasında herhangi bir zamanda, herhangi bir şiddet eylemi sırasında takım üyelerinin katılımını belirlemek için kullanılabilir. İnceleme A1'in B1'e dirseğiyle vurduğunu gösterirse hakemler A1'e sportmenlik dışı faul verebilir. Her iki sportmenlik dışı faul de aynı duran saati periyodunda periyotta meydana gelmiştir. A1’in sayısı geçerli sayılacaktır. Her iki eşit ağırlıklı sportmenlik dışı faul cezaları birbirini iptal edecektir. Oyun başarılı bir sayı sonrasında olduğu gibi B takımının dip çizgisinin gerisinden topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-2 Genel prensipler | F-3.3.19\nAçıklama: Anında/direkt olarak çalınmayan bir şiddet eyleminin meydana geldiği durumlarda hakemler, herhangi olası bir şiddet eylemi veya potansiyel şiddet eylemi için inceleme yapmak amacıyla oyunu herhangi bir zamanda durdurmaya yetkilidirler. Hakemler, Anlık Tekrar Sistemi incelemesi ihtiyacını belirlemeli ve inceleme, hakemler oyunu ilk kez durdurduğunda yapılmalıdır. İncelemesi bir şiddet eylemi gerçekleştiğini belirtirse, hakemler ihlali bildirecek ve şiddet...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Anlık Tekrar Sistemi oyun sırasında herhangi bir zamanda, herhangi bir şiddet eylemi sırasında ekip üyelerinin katılımını belirlemek için kullanılabilir. Eğer inceleme A2'nin B2'ye dirseğiyle vurduğunu gösterirse, hakemler A2'ye sportmenlik dışı faul verebilir. Teknik faulün cezası önce uygulanacaktır. Herhangi bir B takımı veya A takımı oyuncusu dizilmeden 1 serbest atış atacaktır. Daha sonra B2 kimse dizilmeden 2 serbest atış kullanacaktır. Oyun, B takımı tarafından kendi ön sahasındaki topu oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde 14 saniyesi olacaktır.",
                'choices': [
                    ('Teknik faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Faul yok / oyun devam', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.1\nAçıklama: İtiraz hakkını kullanmak isteyen başantrenör en yakınındaki hakemle görsel temasa geçecektir. Başantrenör yüksek sesli olarak İngilizce “Challenge” diyecek ve aynı anda gerekli işareti gösterecektir (elleriyle dikdörtgen çizerek). Bir başantrenör sadece “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabilir. Dördüncü çeyrekte veya uzatmalarda oyun saatinin 2:00 veya daha az göstermesi de dahil...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Başantrenör elleriyle bir dikdörtgen çizerek, resmi/onaylı Başantrenörlerin İtiraz Hakkı işaretini göstermediğinden dolayı B takımına Başantrenörlerin İtiraz Hakkı verilmeyecektir.',
                'choices': [
                    ('Başantrenör elleriyle bir dikdörtgen çizerek, resmi/onaylı Başantrenörlerin İtiraz Hakkı işaretini göstermediğinden dolayı B takımına Başantrenörlerin İtiraz H…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.1\nAçıklama: İtiraz hakkını kullanmak isteyen başantrenör en yakınındaki hakemle görsel temasa geçecektir. Başantrenör yüksek sesli olarak İngilizce “Challenge” diyecek ve aynı anda gerekli işareti gösterecektir (elleriyle dikdörtgen çizerek). Bir başantrenör sadece “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabilir. Dördüncü çeyrekte veya uzatmalarda oyun saatinin 2:00 veya daha az göstermesi de dahil...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Sayıya giden topa veya aksama müdahale durumunda yalnızca hakemlerin bir ihlal kararı vermeleri durumunda itiraz edilebilir. Başantrenörün karara itiraz etme talebi kabul edilmeyecektir.',
                'choices': [
                    ('Sayıya giden topa veya aksama müdahale durumunda yalnızca hakemlerin bir ihlal kararı vermeleri durumunda itiraz edilebilir. Başantrenörün karara itiraz etme t…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.1\nAçıklama: İtiraz hakkını kullanmak isteyen başantrenör en yakınındaki hakemle görsel temasa geçecektir. Başantrenör yüksek sesli olarak İngilizce “Challenge” diyecek ve aynı anda gerekli işareti gösterecektir (elleriyle dikdörtgen çizerek). Bir başantrenör sadece “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabilir. Dördüncü çeyrekte veya uzatmalarda oyun saatinin 2:00 veya daha az göstermesi de dahil...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B takımına Başantrenörlerin İtiraz Hakkı verilmeyecektir. Yalnızca “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabilir. Yürüme ihlallerinin çalınıp çalınmadığına bakılmaksızın itiraz edilemez. Başantrenörlerin İtiraz Hakkı talep eder',
                'choices': [
                    ('Yürüme ihlali (top kaybı)', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.1\nAçıklama: İtiraz hakkını kullanmak isteyen başantrenör en yakınındaki hakemle görsel temasa geçecektir. Başantrenör yüksek sesli olarak İngilizce “Challenge” diyecek ve aynı anda gerekli işareti gösterecektir (elleriyle dikdörtgen çizerek). Bir başantrenör sadece “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabilir. Dördüncü çeyrekte veya uzatmalarda oyun saatinin 2:00 veya daha az göstermesi de dahil...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A takımına Başantrenörlerin İtiraz Hakkı verilecektir. Hakemler her iki takımı da dezavantajlı duruma düşürmeden oyunu derhal durduracaktır. Anlık Tekrar Sistemi incelemesi A1'in şutunda atışın 2 sayılık bölgeden yapıldığını tespit ederlerse oyun A 82 – B 80 skoruyla devam edecektir. Eğer inceleme A1'in şutunun 3 sayılık bölgeden yapıldığını gösterirse oyun A 83 – B 80 skoruyla devam edecektir her iki durumda da oyun B takımı tarafından B1'in top dripling yaptığı sırada oyunun durdurulduğu en yakın yerden oyun saatinde kalan süre ile topun oyuna sokulmasıyla devam edecektir.",
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.1\nAçıklama: İtiraz hakkını kullanmak isteyen başantrenör en yakınındaki hakemle görsel temasa geçecektir. Başantrenör yüksek sesli olarak İngilizce “Challenge” diyecek ve aynı anda gerekli işareti gösterecektir (elleriyle dikdörtgen çizerek). Bir başantrenör sadece “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabilir. Dördüncü çeyrekte veya uzatmalarda oyun saatinin 2:00 veya daha az göstermesi de dahil...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A takımına Başantrenörlerin İtiraz Hakkı verilecektir. Oyun hemen durudurulacaktır. Eğer Anlık Tekrar Sistemi incelemesi A1'in şutunun 2 sayılık bölgeden atıldığını tespit ederse oyun A 82 – B 82 skoruyla, A takımının topu kendi dip çizgisinin gerisinden oyuna sokmasıyla ve oyun saatinde 1 saniyeyle devam edecektir. Eğer inceleme A1'in şutunun 3 sayılık bölgeden atıldığını gösterirse oyun A 83 – B 82 skoruyla, A takımının topu kendi dip çizgisinden oyuna sokmasıyla ve oyun saatinde 1 saniyeyle devam edecektir.",
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.1\nAçıklama: İtiraz hakkını kullanmak isteyen başantrenör en yakınındaki hakemle görsel temasa geçecektir. Başantrenör yüksek sesli olarak İngilizce “Challenge” diyecek ve aynı anda gerekli işareti gösterecektir (elleriyle dikdörtgen çizerek). Bir başantrenör sadece “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabilir. Dördüncü çeyrekte veya uzatmalarda oyun saatinin 2:00 veya daha az göstermesi de dahil...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A takımına Başantrenörlerin İtiraz Hakkı verilecektir. Hakemler maç kağıdını imzalamadan önce Anlık Tekrar Sistemi incelemesini yapacaklardır. Eğer inceleme A1'in şutunun 2 sayılık bölgeden atıldığını gösterirse oyun, pozisyon sırası hakkına göre bir uzatma oynanarak devam edecektir. Eğer inceleme A1'in şutunun 3 sayılık bölgeden atıldığını gösterirse maçın sonucu A 83 – B 82 ile sona ermiştir.",
                'choices': [
                    ('A takımına Başantrenörlerin İtiraz Hakkı verilecektir. Hakemler maç kağıdını imzalamadan önce Anlık Tekrar Sistemi incelemesini yapacaklardır. Eğer inceleme A1…', True),
                    ('A takımına Başantrenörlerin İtiraz Hakkı verilmeyecektir. Hakemler maç kağıdını imzalamadan önce Anlık Tekrar Sistemi incelemesini yapacaklardır. Eğer inceleme A1…', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.1\nAçıklama: İtiraz hakkını kullanmak isteyen başantrenör en yakınındaki hakemle görsel temasa geçecektir. Başantrenör yüksek sesli olarak İngilizce “Challenge” diyecek ve aynı anda gerekli işareti gösterecektir (elleriyle dikdörtgen çizerek). Bir başantrenör sadece “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabilir. Dördüncü çeyrekte veya uzatmalarda oyun saatinin 2:00 veya daha az göstermesi de dahil...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A takımına Başantrenörlerin İtiraz Hakkı verilecektir. Başhakem, yapılan atışın 2 veya 3 sayı olarak sayılıp sayılamayacağına karar vermek için oyunun herhangi bir anında Başantrenörlerin İtiraz Hakkı için Anlık Tekrar Sistemi incelemesini kullanabilir. Eğer inceleme A1'in şutunun 2 sayılık bölgeden atıldığını gösterirse oyun, pozisyon sırası hakkına göre bir uzatma oynanarak devam edecektir. Eğer inceleme A1'in şutunun 3 sayılık bölgeden atıldığını gösterirse maçın sonucu A 83 – B 82 ile sona ermiştir.",
                'choices': [
                    ('A takımına Başantrenörlerin İtiraz Hakkı verilecektir. Başhakem, yapılan atışın 2 veya 3 sayı olarak sayılıp sayılamayacağına karar vermek için oyunun herhangi…', True),
                    ('A takımına Başantrenörlerin İtiraz Hakkı verilmeyecektir. Başhakem, yapılan atışın 2 veya 3 sayı olarak sayılıp sayılamayacağına karar vermek için oyunun herhangi…', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.1\nAçıklama: İtiraz hakkını kullanmak isteyen başantrenör en yakınındaki hakemle görsel temasa geçecektir. Başantrenör yüksek sesli olarak İngilizce “Challenge” diyecek ve aynı anda gerekli işareti gösterecektir (elleriyle dikdörtgen çizerek). Bir başantrenör sadece “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabilir. Dördüncü çeyrekte veya uzatmalarda oyun saatinin 2:00 veya daha az göstermesi de dahil...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B takımına Başantrenörlerin İtiraz Hakkı verilecektir. Anlık Tekrar Sistemi incelemesi, Başantrenörlerin İtiraz Hakkı durumunda oyunun herhangi bir anında saha dışı ihlali kararının doğru olup olmadığına karar vermek için kullanılabilir. Mola süresi, inceleme bitene ve hakem kesin kararını bildirene kadar başlamayacaktır. A takımının mola talebi, hakem son Anlık Tekrar Sistemi kararını bildirene kadar inceleme sırasında herhangi bir zamanda geri çekilebilir.',
                'choices': [
                    ('B takımına Başantrenörlerin İtiraz Hakkı verilecektir. Anlık Tekrar Sistemi incelemesi, Başantrenörlerin İtiraz Hakkı durumunda oyunun herhangi bir anında saha…', True),
                    ('B takımına Başantrenörlerin İtiraz Hakkı verilmeyecektir. Anlık Tekrar Sistemi incelemesi, Başantrenörlerin İtiraz Hakkı durumunda oyunun herhangi bir anında saha…', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.1\nAçıklama: İtiraz hakkını kullanmak isteyen başantrenör en yakınındaki hakemle görsel temasa geçecektir. Başantrenör yüksek sesli olarak İngilizce “Challenge” diyecek ve aynı anda gerekli işareti gösterecektir (elleriyle dikdörtgen çizerek). Bir başantrenör sadece “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabilir. Dördüncü çeyrekte veya uzatmalarda oyun saatinin 2:00 veya daha az göstermesi de dahil...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B takımına Başantrenörlerin İtiraz Hakkı verilmeyecektir. Yalnızca “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabilir. 8 saniye ihlali yalnızca çeyreğin veya uzatmanın sonundaki bir oyun durumu söz konusu olduğunda incelenebilir. Sayı geçerli sayılacaktır. B takımı başantrenörü, hakkı olan 1 Başantrenörlerin İtiraz Hakkını kullanmıştır.',
                'choices': [
                    ('B takımına Başantrenörlerin İtiraz Hakkı verilmeyecektir. Yalnızca “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabil…', True),
                    ('B takımına Başantrenörlerin İtiraz Hakkı verilecektir. Yalnızca “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabil…', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.1\nAçıklama: İtiraz hakkını kullanmak isteyen başantrenör en yakınındaki hakemle görsel temasa geçecektir. Başantrenör yüksek sesli olarak İngilizce “Challenge” diyecek ve aynı anda gerekli işareti gösterecektir (elleriyle dikdörtgen çizerek). Bir başantrenör sadece “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen durumlar için itiraz hakkı kullanabilir. Dördüncü çeyrekte veya uzatmalarda oyun saatinin 2:00 veya daha az göstermesi de dahil...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "A takımına Başantrenörlerin İtiraz Hakkı verilecektir. Anlık Tekrar Sistemi incelemesi oyun sırasında herhangi bir zamanda kişisel faulün sportmenlik dışı faul olarak yükseltilip yükseltilmeyeceğine karar vermek için kullanılabilir. İnceleme B1'in kişisel faulünün sportmenlik dışı faul olduğunu gösterirse B1'in teknik faulü B1'in otomatik olarak diskalifiye edilmesine yol açacaktır. B1'in hakemlere daha fazla kötü davranması nedeniyle diskalifiye edilmesi artık oyunda cezalandırılamaz ve yarışmanın organizasyon birime rapor edilmelidir. Herhangi bir A takımı oyuncusu kimse dizilmeden 1 serbest atış kullanacaktır. Daha sonra A1 kimse dizilmeden 2 serbest atış kullanacaktır. Oyun, A takımının ön sahasındaki oyuna sokma çizgisinden topu oyuna sokmasıyla devam edecektir.",
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.12\nAçıklama: Her iki takımdan birinin molası başladıktan sonra Başantrenörlerin İtiraz Hakkı istendiğinde bu mola ara verilmeden devam edecektir. Başantrenörlerin İtiraz Hakkı talebi iptal edilemez ve mola sonrasında inceleme gerçekleştirilecektir.\nÖrnek F-4.13: A1, 3 sayılık bölgeden başarılı bir sayı girişiminde bulunur. Bu anda B takımı bir mola ister. Mola sırasında B takımı başantrenörü, atış yapan oyuncunun top ellerini terk etmeden önce ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B takımına Başantrenörlerin İtiraz Hakkı verilecektir. Anlık Tekrar Sistemi incelemesi başarılı bir şutun 2 veya 3 sayı bölgesinden atılıp atılmadığına karar vermek için kullanılabilir. Mola ara verilmeden devam edecektir. Başantrenörlerin İtiraz Hakkı incelemesi moladan sonra yapılacaktır.',
                'choices': [
                    ('B takımına Başantrenörlerin İtiraz Hakkı verilecektir. Anlık Tekrar Sistemi incelemesi başarılı bir şutun 2 veya 3 sayı bölgesinden atılıp atılmadığına karar v…', True),
                    ('B takımına Başantrenörlerin İtiraz Hakkı verilmeyecektir. Anlık Tekrar Sistemi incelemesi başarılı bir şutun 2 veya 3 sayı bölgesinden atılıp atılmadığına karar v…', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.14\nAçıklama: Anlık Tekrar Sisteminin kullanıldığı tüm müsabakalarda, başantrenöre yalnızca bir Başantrenörlerin İtiraz Hakkı verilebilir. “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen zaman kısıtlamaları geçerli değildir.\nÖrnek F-4.15: İkinci çeyrekte oyun saatinde 3:23 kala top saha dışına çıkar. Hakemler topu A takımına verir. B takımı başantrenörü kararın doğru olmadığına inanır ve uygun prosedürü kullanarak Başantrenörlerin İtiraz ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': '(a) Başantrenörlerin İtiraz Hakkı verilecektir. Başhakem oyunun herhangi bir anında saha dışı ihlali kararının doğru olup olmadığına karar vermek için Anlık Tekrar Sistemini kullanılabilir. Eğer inceleme kararın doğru olduğunu gösterirse oyun A takımının topu oyuna sokmasıyla devam edecektir. Eğer inceleme sonucunda kararın doğru olmadığı tespit edilirse karar düzeltilecektir. Oyun B takımının topu oyuna sokmasıyla devam edecektir. Her iki durumda da B takımı başantrenörü hakkı olan 1. Başantrenörlerin İtiraz Hakkını kullanmıştır. (b) B takımı başantrenörü hakkı olan 1 Başantrenörlerin İtiraz Hakkını zaten kullanmıştır. Talep kabul edilmeyecektir.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.14\nAçıklama: Anlık Tekrar Sisteminin kullanıldığı tüm müsabakalarda, başantrenöre yalnızca bir Başantrenörlerin İtiraz Hakkı verilebilir. “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen zaman kısıtlamaları geçerli değildir.\nÖrnek F-4.16: İkinci çeyrekte oyun saatinde 3:21 kala top saha dışına çıkar. Hakemler topu A takımına verir. B takımı başantrenörü kararın doğru olmadığına inanır ve uygun prosedürü kullanarak Başantrenörlerin İtiraz ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Başantrenörlerin İtiraz Hakkı verildiğinde, itiraz talebi kesindir ve vazgeçilemez.',
                'choices': [
                    ('Başantrenörlerin İtiraz Hakkı verildiğinde, itiraz talebi kesindir ve vazgeçilemez.', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.14\nAçıklama: Anlık Tekrar Sisteminin kullanıldığı tüm müsabakalarda, başantrenöre yalnızca bir Başantrenörlerin İtiraz Hakkı verilebilir. “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen zaman kısıtlamaları geçerli değildir.\nÖrnek F-4.17: İkinci çeyrekte oyun saatinde 2:35 kala A1 şut saati periyodunun sonuna doğru bir sayı atar ve oyun devam eder. B takımı başantrenörü şut saati sesli işaretinin top elden çıkmadan önce çaldığına inanmakt...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "B takımına Başantrenörlerin İtiraz Hakkı verilecektir. Anlık Tekrar Sistemi incelemesi oyunun herhangi bir anında şut saati sesli işaretinden önce topun A1'in ellerinden çıkıp çıkmadığına karar vermek için kullanılabilir. Oyunun herhangi bir anında Başantrenörlerin İtiraz Hakkı talep edilebilir. Hakemlerin oyunu derhal durdurma ve inceleme yapma yetkisi vardır. Eğer incelemede topun şut saati sesli işareti vermeden önce elden çıktığı tespit edilirse, sayı geçerli sayılacaktır. Oyun, oyun durdurulduğunda topun bulunduğu en yakın yerden B takımının topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde kalan süresi kadar zamanı olacaktır. Eğer incelemede topun şut saati sesli işaretinin çalmasından sonra elden çıktığı tespit edilirse, sayı geçerli sayılmayacaktır. Oyun, oyun durdurulduğunda topun bulunduğu en yakın yerden B takımının topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde kalan süresi olacaktır. Her iki durumda da B takımı başantrenörü hakkı olan 1. Başantrenörlerin İtiraz Hakkını kullanmıştır.",
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.14\nAçıklama: Anlık Tekrar Sisteminin kullanıldığı tüm müsabakalarda, başantrenöre yalnızca bir Başantrenörlerin İtiraz Hakkı verilebilir. “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen zaman kısıtlamaları geçerli değildir.\nÖrnek F-4.18: İkinci çeyrekte oyun saatinde 2:29 kala A1 şut saati periyodunun sonuna doğru bir sayı atar ve oyun devam eder. A2 topun saha dışına çıkmasına neden olduğunda hakemler B takımının ön sahasında oyunu durd...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': "Başantrenörlerin İtiraz Hakkı oyunun herhangi bir anında, en geç hakemlerin karardan sonra oyunu ilk kez durdurması durumunda talep edilebilir. B takımına Başantrenörlerin İtiraz Hakkı verilecektir. Anlık Tekrar Sistemi incelemesi şut saati sesli işaretinden önce topun A1'in ellerinden çıkıp çıkmadığına karar vermek için kullanılabilir. Eğer incelemede topun şut saati sesli işaretini vermeden önce elden çıktığı tespit edilirse, sayı varsa geçerli sayılacaktır. Eğer incelemede topun şut saati sesli işaretinin çalmasından sonra elden çıktığı tespit edilirse, sayı geçerli sayılmayacaktır. Her iki durumda da oyun, topun saha dışına çıktığı en yakın yerden B takımının topu oyuna sokmasıyla devam edecektir. B takımının şut saatinde kalan süresi kadar zamanı olacaktır. B takımı baş antrenörü, hakkı olan 1 mücadeleyi kullandı. B takımı başantrenörü hakkı olan 1. Başantrenörlerin İtiraz Hakkını kullanmıştır.",
                'choices': [
                    ('Top B takımına verilir (oyuna sokma)', True),
                    ('Top B takımında (B oyuna sokar)', False),
                    ('Top A takımında (A oyuna sokar)', False),
                ]
            },
            {
                'text': "F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.14\nAçıklama: Anlık Tekrar Sisteminin kullanıldığı tüm müsabakalarda, başantrenöre yalnızca bir Başantrenörlerin İtiraz Hakkı verilebilir. “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen zaman kısıtlamaları geçerli değildir.\nÖrnek F-4.19: Üçüncü çeyrekte oyun saatinde 7:22 kala B1, dripling yapan A1'e faul yapar. Bu, B takımının bu çeyrekteki ikinci faulüdür. A takımı başantrenörü, kurallara uygun olarak doğrudan topla oynamaya yönelik bi...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'A takımına Başantrenörlerin İtiraz Hakkı verilecektir. Anlık Tekrar Sistemi incelemesi, oyunun herhangi bir anında kişisel faulün, sportmenlik dışı faulün veya diskalifiye edici faulün yükseltilip yükseltilmeyeceğine, düşürüleceğine veya teknik faul olarak değerlendirilip değerlendirilmeyeceğine karar vermek için kullanılabilir. Eğer inceleme faulün kişisel faul olduğunu gösterirse oyun, kişisel faul çalındığında topun bulunduğu en yakın yerden A takımının topu oyuna sokmasıyla devam edecektir. Eğer incelemede kişisel faulün sportmenlik dışı faul olduğu tespit edilirse, kişisel faul kararı yükseltecektir. Oyun diğer sportmenlik dışı faullerden sonra olduğu gibi devam edecektir. Her iki durumda da B takımı başantrenörü hakkı olan 1. Başantrenörlerin İtiraz Hakkını kullanmıştır.',
                'choices': [
                    ('Diskalifiye edici faul', True),
                    ('Sportmenlik dışı faul', False),
                    ('Teknik faul', False),
                ]
            },
            {
                'text': "F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.14\nAçıklama: Anlık Tekrar Sisteminin kullanıldığı tüm müsabakalarda, başantrenöre yalnızca bir Başantrenörlerin İtiraz Hakkı verilebilir. “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen zaman kısıtlamaları geçerli değildir.\nÖrnek F-4.20: Üçüncü çeyrekte oyun saatinde 7:16 kala (a) B1, dripling yapan A1'e faul yapar. Bu, B takımının bu çeyrekteki ikinci faulüdür. Oyun A takımının topu oyuna sokmasıyla devam eder. Daha sonra A2, 2 sayılık ...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?",
                'explanation': 'A takımına Başantrenörlerin İtiraz Hakkı verilmeyecektir. Top A takımı oyuncusunun kullanımına geçtikten sonra (a) topu oyuna sokmak, (b) ilk serbest atış, Başantrenörlerin İtiraz Hakkının verilmesi için artık çok geçtir. Başantrenör, en geç hakemlerin karardan sonra oyunu ilk kez durdurduğunda ve top yeniden canlanmadan önce Başantrenörlerin İtiraz Hakkı ve Anlık Tekrar Sistemi incelemesi gerçekleştirilmelidir. A takımı başantrenörü hakkı olan 1. Başantrenörlerin İtiraz Hakkını kullanmamıştır.',
                'choices': [
                    ('Top A takımına verilir (oyuna sokma)', True),
                    ('Top A takımında (A oyuna sokar)', False),
                    ('Top B takımında (B oyuna sokar)', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.14\nAçıklama: Anlık Tekrar Sisteminin kullanıldığı tüm müsabakalarda, başantrenöre yalnızca bir Başantrenörlerin İtiraz Hakkı verilebilir. “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen zaman kısıtlamaları geçerli değildir.\nÖrnek F-4.21: Şut saati periyodunun sonuna doğru A1 bir sayı atar ve oyun devam eder. B takımının başantrenör yardımcısı, şut atılmadan önce şut saati sesli işareti verdiğine inanır ve doğru prosedürü kullanarak bir B...\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'B takımının birinci antrenör yardımcısının talebi kabul edilmeyecektir. Anlık Tekrar Sistemi incelemesi yalnızca B takımı başantrenörü tarafından talep edilebilir.',
                'choices': [
                    ('B takımının birinci antrenör yardımcısının talebi kabul edilmeyecektir. Anlık Tekrar Sistemi incelemesi yalnızca B takımı başantrenörü tarafından talep edilebi…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
            {
                'text': 'F-4 Başantrenörlerin İtiraz Hakkı (Challenge) | F-4.14\nAçıklama: Anlık Tekrar Sisteminin kullanıldığı tüm müsabakalarda, başantrenöre yalnızca bir Başantrenörlerin İtiraz Hakkı verilebilir. “Resmi Basketbol Yorumları Ek Bölüm F-3” te belirtilen zaman kısıtlamaları geçerli değildir.\nÖrnek F-4.22: Sayı görevlisi, talep edilen tüm takım Başantrenörlerin İtiraz Hakkı taleplerini maç kağıdına girecektir.\n\nAşağıdaki örneğe göre bu durumda doğru karar hangisidir?',
                'explanation': 'Maç kağıdında Başantrenörlerin İtiraz Hakkı yanındaki 2 kutuya yalnızca kullanılan Başantrenörlerin İtiraz Hakkı girilecektir. Sayı görevlisi ilk kutuya çeyreği veya uzatmayı, ikinci kutuya ise çeyrek veya uzatmadaki oyun süresinin dakikasını yazacaktır.',
                'choices': [
                    ('Maç kağıdında Başantrenörlerin İtiraz Hakkı yanındaki 2 kutuya yalnızca kullanılan Başantrenörlerin İtiraz Hakkı girilecektir. Sayı görevlisi ilk kutuya çeyreğ…', True),
                    ('Yukarıdakilerin hiçbiri', False),
                ]
            },
        ]

        # Get the maximum order number for existing questions in this session
        max_order = Question.objects.filter(session=session).aggregate(
            max_order=Max('order')
        )['max_order'] or 0

        # Add questions
        added_count = 0
        for idx, q_data in enumerate(questions_data, start=1):
            order = max_order + idx
            
            # Check if question already exists (by text)
            question, created = Question.objects.get_or_create(
                session=session,
                text=q_data['text'],
                defaults={'order': order, 'is_active': True, 'explanation': q_data.get('explanation', '')}
            )
            
            if created:
                # Add choices
                for choice_text, is_correct in q_data['choices']:
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=is_correct
                    )
                added_count += 1
                # Safe encoding for display
                try:
                    display_text = q_data["text"][:50].encode('ascii', errors='replace').decode('ascii')
                except:
                    display_text = f"Question {idx}"
                self.stdout.write(f'  Added question {idx}: {display_text}...')
            else:
                # Update explanation if it exists
                if q_data.get('explanation') and not question.explanation:
                    question.explanation = q_data['explanation']
                    question.save(update_fields=['explanation'])
                # Safe encoding for display
                try:
                    display_text = q_data["text"][:50].encode('ascii', errors='replace').decode('ascii')
                except:
                    display_text = f"Question {idx}"
                self.stdout.write(f'  Question {idx} already exists: {display_text}...')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {len(questions_data)} questions. '
                f'{added_count} new questions added, {len(questions_data) - added_count} already existed.'
            )
        )
