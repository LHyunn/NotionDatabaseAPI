설명
---

코드를 사용하여 노션 데이터베이스에 데이터를 올리는 방법은 다음과 같습니다.

NotionDatabase 클래스의 인스턴스를 생성합니다.

```python
database_id = "<데이터베이스 ID>"
notion_key = "<노션 API 키>"
notion_db = NotionDatabase(database_id, notion_key)
```

위 코드에서 <데이터베이스 ID>와 <노션 API 키>는 실제 노션 데이터베이스의 ID와 노션 API 키로 대체되어야 합니다. 또한, 데이터베이스에 API Bot이 추가되어있어야 합니다. 자세한 내용은 https://www.notion.so/ko-kr/help/category/import-export-and-integrate 를 참고하세요.

>데이터베이스 ID는 데이터베이스의 주소 : https://www.notion.so/id/a?v=b 에서 a의 위치에 존재합니다.

![title](https://user-images.githubusercontent.com/74236661/252056154-c250bf71-3010-46f0-b0a5-55027a928d05.png) 

print_property_dict 메서드를 사용하여 노션 데이터베이스의 프로퍼티를 가져옵니다. 


```python
notion_db.print_property_dict()
```




```python
{
  'Accuracy': 'number',
  'Batch Size': 'select',
  'Class Weight': 'rich_text',
  'Dataset': 'select',
  'F1 Score': 'number',
  'Input Size': 'select',
  'Learning Rate': 'number',
  'Loss Func': 'select',
  'Model': 'title',
  'Precision': 'number',
  'Recall': 'number',
  'Threshold': 'number',
  '상태': 'status',
  '성능지표 합': 'formula',
  '실행 일시': 'date',
  '테스트 일시': 'created_time'
}
```

위 딕셔너리는 업로드할 데이터를 나타냅니다. 각 키는 노션 데이터베이스의 속성 이름과 일치해야 하고, 값은 해당 속성에 업로드할 데이터를 나타내야 합니다. 속성 중 formula와 created_time은 노션에서 관리됩니다. 현재 입력이 가능한 속성은 select, status, date, rich_text, title, number 입니다.

노션에서 사용하는 날짜의 형식은 2023-01-01T00:00:00.000+09:00 입니다. 필요하다면 제공하는 메서드를 사용하여 쉽게 변환할 수 있습니다.


```python
DATE = notion_db.transform_date("20230101000000")
# 2023-01-01T00:00:00.000+09:00
```

데이터를 노션에 업로드합니다.




```python
page_values = {
    "Model": "model_name",
    "Dataset": "Dataset",
    "Input Size": "Input_Size",
    "Batch Size": "Batch_Size",
    "Learning Rate": 0.5,
    "Loss Func": "Loss_Function",
    "Class Weight": "(0:1, 1:1)",
    "Threshold": 0.5,
    "Precision": 0.5,
    "Recall": 0.5,
    "F1 Score": 0.5,
    "Accuracy": 0.5,
    "상태": "Done",
    "실행 일시": DATE
}

notion_db.upload_page_values(page_values)
    
```

위 코드는 upload_page_values 메서드를 사용하여 데이터를 노션에 업로드합니다.

page_values 딕셔너리의 키와 값을 업로드하려는 데이터에 맞게 수정해야 합니다.

![title](https://user-images.githubusercontent.com/74236661/252056147-66d3fdc7-6bc5-4212-b312-30b0213dc471.png)

