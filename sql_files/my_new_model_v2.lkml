connection: "external_small"

### Owner - Tal ###

include: "/**/*.view.lkml"                 # include all views in this project
include: "/**/*.dashboard.lookml"   # include a LookML dashboard called my_dashboard

week_start_day: sunday

# Explores
# Policy Checkout Details
explore: my_new_explore {
        access_filter: {field: dima_table.merchant_id
                          user_attribute: merchant
                          }
}
