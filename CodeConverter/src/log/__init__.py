if __name__=="__main__":
    import sys
    print(sys.path)
    from util.connection import connectionUtil
    from bean.entitys import Property
    from util.codeutils import codeutil
    conn=connectionUtil.getConnection("com.mysql.jdbc.Driver", "jdbc:mysql://localhost:3306/test", "root", "root")
    db=Database()
    proc=db.getProcedure(conn, 'test', 'test_proc')
    table=db.getTable(conn, 'columns', 'pet')
    properties=[]
    classes=set()
    c_name=codeutil.convert2property(table.get_name())
    for item in table.get_columns():
        p_name=item.get_name()
        c_type=item.get_c_type()
        c_types=c_type.split('.')
        type=c_type
        if len(c_types)>1:
            classes.add(c_type)
            type=c_types[len(c_types)-1]
        prop=Property(False,p_name,type)
        properties.append(prop)
    bean=Class(c_name,'com.entity',classes,'',{},properties)
    data={"classBean":bean}
    str=codeutil.template("java_bean.html", data)
    print(str)
    
    
    