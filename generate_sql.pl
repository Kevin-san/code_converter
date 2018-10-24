#!/opt/perl/5.8.5/bin/perl
#ident	"%W%"

my $feed = $ARGV[0];
my $outputSql = $ARGV[1];
my $requireConfig = $ARGV[2];
my $sqlTemplate = $ARGV[3];
require "$requireConfig";
require "$sqlTemplate";

my $action = $templates{action};
my @columns = @{$templates{columns}};
my $leng = @columns;
print "@columns\n";
my @indexes = @{$config{indexes}};
my $excludeRows = $config{excludeRows};
my @all_columns = @{$config{all_columns}};
my $table = $templates{table};
my @template = @{$templates{template}};
my @column_type = @{$templates{column_type}};
my %column_indexes = create_map(\@all_columns,\@indexes);
my %column_types = create_map(\@columns,\@column_type);
my %column_template = create_map(\@columns,\@template);
my @result = read_csv_file($feed,$excludeRows,\%column_indexes);
open(SQL, ">$outputSql") or die "Failed to open File outputSql file $!";
if($action eq "insert"){
	my $length = @result;
	print "$length\n";
	for(my $idx=0;$idx<$length;$idx++){
		my %values = %{$result[$idx]};
		my $sql=create_insert_sql($table,\@columns,\%values,\%column_types,\%column_template);
		print SQL "$sql;\n";
	}
}elsif($action eq "update"){
	my $length = @result;
	print "$length\n";
	my @updateColumns=@{$templates{updateColumns}};
	my @updateValues=@{$templates{updateValues}};
	my $masterTable = $templates{masterTable};
	my $defConditions = $templates{defConditions};
	my @conditionColumns=@{$templates{conditionColumns}};
	my @conditionTemplate=@{$templates{conditionTemplate}};
	my %updateValues = create_map(\@updateColumns,\@updateValues);
	my %conditionTemplate = create_map(\@conditionColumns,\@conditionTemplate);
	for(my $idx=0;$idx<$length;$idx++){
		my %values = %{$result[$idx]};
		my $sql=create_update_sql($table,$masterTable,$defConditions,\@updateColumns,\@conditionColumns,\%updateValues,\%values,\%column_types,\%column_template,\%conditionTemplate);
		if($sql ne ""){
			print SQL "$sql;\n";
		}
	}
}
#elsif($action eq "oraupdate"){
#	my $length = @result;
#	print "$length\n";
#	my @updateColumns=@{$templates{updateColumns}};
#	my @updateValues=@{$templates{updateValues}};
#	my $masterTable = $templates{masterTable};
#	my $defConditions = $templates{defConditions};
#	my @conditionColumns=@{$templates{conditionColumns}};
#	my @conditionTemplate=@{$templates{conditionTemplate}};
#	my %updateValues = create_map(\@updateColumns,\@updateValues);
#	my %conditionTemplate = create_map(\@conditionColumns,\@conditionTemplate);
#	for(my $idx=0;$idx<$length;$idx++){
#		my %values = %{$result[$idx]};
#		my $sql=create_oracle_update_sql($table,$masterTable,$defConditions,\@updateColumns,\@conditionColumns,\%updateValues,\%values,\%column_types,\%column_template,\%conditionTemplate);
#		print SQL "$sql;\n";
#	}
#}
#elsif($action eq "inselect"){
#	my $length = @result;
#	print "$length\n";
#	my @selectColumns=@{$templates{selectColumns}};
#	my @selectValues=@{$templates{selectValues}};
#	my $selectTable = $templates{selectTable};
#	my @conditionColumns=@{$templates{conditionColumns}};
#	my @conditionTemplate=@{$templates{conditionTemplate}};
#	my %selectValues = create_map(\@selectColumns,\@selectValues);
#	my %conditionTemplate = create_map(\@conditionColumns,\@conditionTemplate);
#	for(my $idx=0;$idx<$length;$idx++){
#		my %values = %{$result[$idx]};
#		my $sql = create_insert_select_sql($table,$selectTable,\@columns,\%values,\%column_types,\%column_template,\%selectValues,\@conditionColumns,\%conditionTemplate);
#		print SQL "$sql;\n";
#	}
#}

close(SQL);

sub read_csv_file($$%){
	my $file = $_[0];
	my $excludeRows = $_[1];
	my %indexs = %{$_[2]};
	open(FILE, "$file") or die "Failed to open File source file $!";
	my @result = ();
	my $excludeRow = $excludeRows -1;
	for(0..$excludeRow){
		<FILE>;
	}
	while (<FILE>) {
		my @array=split_csv($_);
		my %arr = ();
		for(keys %indexs){
			$arr{$_} = $array[$indexs{$_}-1];
		}
		push @result,\%arr;
	}
	return @result;
}
sub replace($$$){
	my $line = $_[0];
	my $rep = $_[1];
	my $type = $_[2];
	my $str = $line;
	if($rep eq "null"){
		$line =~ s/\?/NULL/;
	}
	if($type eq "str"){
		$line =~ s/\?/\'$rep\'/;
	}else{
		$line =~ s/\?/$rep/;
	}
	if($str eq $line && $type eq "str"){
		$line = "\'$line\'";
	}
	return $line;
}

sub compareLength(@@){
	my @original = @{$_[0]};
	my @compare = @{$_[1]};
	my $length = @original;
	my $len = @compare;
	my $boo=($length == $len);
	print "$len,$length,$boo\n";
	return $length == $len;
}

sub create_map(@@){
	my @keys = @{$_[0]};
	my @values = @{$_[1]};
	my %resultMap = ();
	if(compareLength(\@keys,\@values)){
		my $length = @keys;
		for(my $i=0;$i<$length;$i++){
			$resultMap{$keys[$i]}=$values[$i];
		}
	}
	return %resultMap;
}

sub merge_two_maps(%%){
	my %first=%{$_[1]};
	my %second=%{$_[2]};
	my %resMap = ();
	for(keys %first){
		$resMap{$_}=$first{$_};
	}
	for(keys %second){
		$resMap{$_}=$second{$_};
	}
	return %resMap;
}

sub split_csv($){
	my $line = $_[0];
	my @array = split(/\|/,$line);
	my @line = ();
	my $length = @array;
	for(my $i=0;$i<$length;$i++){
		my $item = $array[$i];
		my $nextItem = $array[++$i];
		if ($item =~ /^\"/ && $nextItem =~ /\"$/){
			$item =~ s/^\"//g;
			$nextItem =~ s/\"$//g;
			$item ="${item},${nextItem}";
		}elsif($item =~ /^\'/ && $nextItem =~ /\'$/){
			$item =~ s/^\'//g;
			$nextItem =~ s/\'$//g;
			$item ="${item},${nextItem}";
		}else{
			--$i;
		}
		$item=~ s/\r|\n$//g;
		push @line,$item;
	}
	return @line;
}
sub create_cols_str(@){
	my @columns=@{$_[0]};
	my $cols_str = "";
	my $CUMMA = ", ";
	my $leng = @columns;
	for(my $id=0;$id<$leng;$id++){
		my $column_key = $columns[$id];
		$cols_str .= $column_key.$CUMMA;
	}
	$cols_str =~ s/$CUMMA$//;
	return $cols_str;
}

sub create_values_str(@%%%){
	my @columns=@{$_[0]};
	my %values = %{$_[1]};
	my %types=%{$_[2]};
	my %templates = %{$_[3]};
	my $values_str = "";
	my $CUMMA = ", ";
	my $leng = @columns;
	for(my $id=0;$id<$leng;$id++){
		my $column_key = $columns[$id];
		my $temp_line = $templates{$column_key};
		my $val = $values{$column_key};
		my $type = $types{$column_key};
		my $item = replace($temp_line,$val,$type);
		$values_str = "${values_str}${item}${CUMMA}";
	}
	$values_str =~ s/$CUMMA$//;
	return $values_str;
}

sub create_conditions_str(@%%%){
	my @columns=@{$_[0]};
	my %values = %{$_[1]};
	my %types=%{$_[2]};
	my %templates = %{$_[3]};
	my $conds_str = "";
	my $leng = @columns;
	for(my $id=0;$id<$leng;$id++){
		my $column_key = $columns[$id];
		my $temp_line = $templates{$column_key};
		my $val = $values{$column_key};
		my $type = $types{$column_key};
		my $item = replace($temp_line,$val,$type);
		$conds_str = "${conds_str} ${item}";
	}
	return $conds_str;
}

sub create_insert_sql($@%%%){
	my $table=$_[0];
	my @columns=@{$_[1]};
	my %values = %{$_[2]};
	my %types=%{$_[3]};
	my %templates = %{$_[4]};
	my $cols_str = create_cols_str(\@columns);
	my $values_str = create_values_str(\@columns,\%values,\%types,\%templates);
	return "insert into ${table}(${cols_str}) values(${values_str})";
}

sub create_oracle_update_sql($$$@@%%%%%){
	my $table=$_[0];
	my $masterTable = $_[1];
	my $defCondition = $_[2];
	my @updateColumns=@{$_[3]};
	my @conditionColumns = @{$_[4]};
	my %updateValues=%{$_[5]};
	my %values = %{$_[6]};
	my %types = %{$_[7]};
	my %templates = %{$_[8]};
	my %conditionTemplates = %{$_[9]};
	my $updLength = @updateColumns;
	if($updLength==0){
		return '';
	}
	my $start_update_sql = "update $table set ";
	if($masterTable eq ""){
		my $update_body_str = create_update_body_str($table,\@updateColumns,\%updateValues,\%types,\%templates);
		my $condition_str = create_conditions_str(\@conditionColumns,\%values,\%types,\%conditionTemplates);
		return "$start_update_sql $update_body_str where $condition_str";
	}else{
		my $cols_str = create_cols_str(\@updateColumns);
		my $child_select_str = "select $cols_str from $masterTable where $defCondition";
		my $condition_str = create_conditions_str(\@conditionColumns,\%values,\%types,\%conditionTemplates);
		if($updLength >1){
			return "${start_update_sql}($cols_str)=($child_select_str) where $condition_str";
		}else{
			return "${start_update_sql} $updateColumns[0]=($child_select_str) where $condition_str";
		}
	}
}
sub create_update_sql($$$@@%%%%%){
	my $table=$_[0];
	my $masterTable = $_[1];
	my $defCondition = $_[2];
	my @updateColumns=@{$_[3]};
	my @conditionColumns = @{$_[4]};
	my %updateValues=%{$_[5]};
	my %values = %{$_[6]};
	my %types = %{$_[7]};
	my %templates = %{$_[8]};
	my %conditionTemplates = %{$_[9]};
	my $updLength = @updateColumns;
	if($updLength==0){
		return '';
	}
	my $start_update_sql = "update $table set ";
	my $update_body_str = create_update_body_str($table,\@updateColumns,\%updateValues,\%types,\%templates);
	my $condition_str = create_conditions_str(\@conditionColumns,\%values,\%types,\%conditionTemplates);
	if($masterTable eq ""){
		return "$start_update_sql $update_body_str where $condition_str";
	}
	return "$start_update_sql $update_body_str from $masterTable where $defCondition and $condition_str";
}

sub create_update_body_str($@%%%){
	my $table=$_[0];
	my @updateColumns=@{$_[1]};
	my %updateValues=%{$_[2]};
	my %types = %{$_[3]};
	my %templates = %{$_[4]};
	my $leng = @updateColumns;
	my $body_str = "";
	my $CUMMA=",";
	for(my $id=0;$id<$leng;$id++){
		my $column_key = $updateColumns[$id];
		my $column_value = $updateValues{$column_key};
		if(exists($types{$column_key})){
			my $temp_line = $templates{$column_key};
			my $type = $types{$column_key};
			my $item = replace($temp_line,$column_value,$type);
		}
		$body_str.= "${table}.${column_key} = $column_value ,";
	}
	$body_str =~ s/$CUMMA$//;
	return $body_str;
}

sub create_insert_select_begin_part($@%%%%){
	my $table=$_[0];
	my @columns=@{$_[1]};
	my %values = %{$_[2]};
	my %types=%{$_[3]};
	my %templates = %{$_[4]};
	my %selectValues=%{$_[5]};
	my $cols_str = create_cols_str(\@columns);
	my $values_str = create_values_str(\@columns,\%values,\%types,\%templates);
	my $CUMMA=",";
	$cols_str.=$CUMMA;
	$values_str.=$CUMMA;
	for(keys %selectValues){
		$cols_str .= $_.$CUMMA;
		$values_str .= $selectValues{$_}.$CUMMA;
	}
	$cols_str =~ s/$CUMMA$//;
	$values_str =~ s/$CUMMA$//;
	
	return "insert into ${table}(${cols_str}) select ${values_str} from ";
}

sub create_insert_select_end_part($@%%%){
	my $table=$_[0];
	my @columns=@{$_[1]};
	my %values = %{$_[2]};
	my %types=%{$_[3]};
	my %templates = %{$_[4]};
	my $conditions_str = create_conditions_str(\@columns,\%values,\%types,\%templates);
	return "$table where $conditions_str";
}

sub create_insert_select_sql($$@%%%%@%){
	my $table=$_[0];
	my $selectTable = $_[1];
	my @columns=@{$_[2]};
	my %values = %{$_[3]};
	my %types=%{$_[4]};
	my %templates = %{$_[5]};
	my %selectTempalte=%{$_[6]};
	my @conditionColumns = @{$_[7]};
	my %conditionTemplate = %{$_[8]};
	my $begin_part = create_insert_select_begin_part($table,\@columns,\%values,\%types,\%templates,\%selectTempalte);
	my $end_part = create_insert_select_end_part($selectTable,\@conditionColumns,\%values,\%types,\%conditionTemplate);
	my $sql = "${begin_part}${end_part}";
	return $sql;
}
