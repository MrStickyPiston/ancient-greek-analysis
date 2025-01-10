fn noun_routs(){
    let logos_roots = vec![
        "ἀνθρώπος",
        "δαίμονος",
        "ἔθνος",
        "κῆπος",
        "κύκλος",
        "λόγος",
        "μῦθος",
        "νόμος",
        "ποταμός",
        "στόλος",
        "τρόπος",
    ];

    for root in logos_roots {
        let new_root = noun_roots_table::ActiveModel {
            root: ActiveValue::Set(root.to_owned()),
            conjugation_group: ActiveValue::Set("λόγος".to_owned()),
            ..Default::default()
        };

        new_root.save(&db).await?;
    }
}