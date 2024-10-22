from deepface import DeepFace

def face_analiz_age(photo):
    try :
        result = DeepFace.analyze(img_path = photo,actions = ["age"])
        print(result)
        return result
    except:
        print("error,отправте другую фотографию для анализа")
        return "error,отправте другую фотографию для анализа"
def face_analiz_emotion(photo):
    try :
        result = DeepFace.analyze(img_path = photo ,actions = ["emotion"])
        print(result)
        return result
    except:
        print("error,отправте другую фотографию для анализа")
        return "error,отправте другую фотографию для анализа"
def face_analiz_race(photo):
    try :
        result = DeepFace.analyze(img_path = photo,actions = ["race"])
        print(result)
        return result
    except:
        print("error,отправте другую фотографию для анализа")
        return "error,отправте другую фотографию для анализа"

def face_analiz_gender(photo):
    try :
        result = DeepFace.analyze(img_path = photo,actions = ["gender"])
        print(result)
        return result
    except:
        print("error,отправте другую фотографию для анализа")
        return "error,отправте другую фотографию для анализа"
def face_analiz_info(photo):
    try :
        result = DeepFace.analyze(img_path = photo,actions = ["emotion",'age','gender','race'])
        print(result)
        return result
    except:
        print("error,отправте другую фотографию для анализа")
        return "error,отправте другую фотографию для анализа"
